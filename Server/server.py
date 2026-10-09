import sqlite3 #Database library
import hashlib #Hashing library
import threading #Treading libray
import socket #Library for network communication
import ssl
import time #Module for working with time values
import random #Library for working with random numbers or objects
import unicodedata
import hmac, os
import secrets
import json
import struct
import sys
from contextlib import contextmanager
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from Server.protocol import MAX_FRAME
from Config.config import BIND_HOST, PORT

USER_DATABASE_PATH = PROJECT_DIR / "Database" / "userdatabase.db"
CARDS_DATABASE_PATH = PROJECT_DIR / "Database" / "cards.db"
PACKS = {10000: 10, 25000: 30, 45000: 50} #Server-side price list: pack cost -> number of cards in the pack
QUICK_SELL_VALUE = 1000 #Coins given for each quick sold duplicate
CLIENT_VERSION = 1
CLIENT_UPDATE_MESSAGE = "Please update your client to the latest version."
SESSION_TTL_SECONDS = 24 * 60 * 60
GAME_CLEANUP_INTERVAL_SECONDS = 60
GAME_IDLE_TTL_SECONDS = 5 * 60
SERVER_CERT_ENV = "GAME_TLS_CERTFILE"
SERVER_KEY_ENV = "GAME_TLS_KEYFILE"
LOCAL_ENV_FILE = PROJECT_DIR / ".env"
GAME_STATS = {
    "Pace": "PAC",
    "Shooting": "SHO",
    "Passing": "PAS",
    "Dribbling": "DRI",
    "Defending": "DEF",
    "Physical": "PHY",
}


def load_local_environment(env_path):
    if not env_path.is_file():
        return
    for line_number, raw_line in enumerate(
        env_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ValueError(
                f"Invalid environment setting on line {line_number} of {env_path}"
            )
        key, value = (part.strip() for part in line.split("=", 1))
        if key not in {SERVER_CERT_ENV, SERVER_KEY_ENV}:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        os.environ.setdefault(key, value)


load_local_environment(LOCAL_ENV_FILE)


def normalize_card_search(value):
    normalized = unicodedata.normalize("NFKD", value.casefold())
    return "".join(
        character
        for character in normalized
        if not unicodedata.combining(character)
    )

@contextmanager
def user_db():
    conn = sqlite3.connect(USER_DATABASE_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def attach_cards_db(conn):
    conn.execute("ATTACH DATABASE ? AS cards_db", (str(CARDS_DATABASE_PATH),))


def hash_password(password):
    salt = os.urandom(16)
    h = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)
    return f"scrypt${salt.hex()}${h.hex()}"

def verify_password(password, stored):
    if stored.startswith("scrypt$"):
        _, salt_hex, hash_hex = stored.split("$")
        h = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1)
        return hmac.compare_digest(h.hex(), hash_hex), False
    ok = hmac.compare_digest(hashlib.sha256(password.encode()).hexdigest(), stored)
    return ok, ok

DUMMY_HASH = hash_password("dummy")

class server: #Class of the main server application
    def __init__(self):
        self.lock = threading.Lock()
        self.sessions = {}
        self.api_player_games = {}
        self.api_game_meta = {}
        self.api_waiting_game = None
        self.api_next_game_id = 0
        self.game_accounts = {}
        
        certfile = os.environ.get(SERVER_CERT_ENV)
        keyfile = os.environ.get(SERVER_KEY_ENV)
        if not certfile or not keyfile:
            raise RuntimeError(
                f"Set {SERVER_CERT_ENV} and {SERVER_KEY_ENV} in "
                f"{LOCAL_ENV_FILE} or the process environment to enable TLS"
            )
        cert_path = Path(certfile)
        key_path = Path(keyfile)
        if not cert_path.is_absolute():
            cert_path = PROJECT_DIR / cert_path
        if not key_path.is_absolute():
            key_path = PROJECT_DIR / key_path
        self.tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.tls_context.load_cert_chain(
            certfile=str(cert_path), keyfile=str(key_path)
        )
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener = server_socket
        self.listener.bind((BIND_HOST, PORT))
        print("Waiting for a connection")
        print("This is the ip: ", BIND_HOST)
        print("This is the port: ", PORT)
        self.listener.listen()
        self.api_server_thread = threading.Thread(target=self.api_server_accept)
    
    def start(self): #Function to start each thread
        self.api_server_thread.start()
        self.game_cleanup_thread = threading.Thread(
            target=self.api_game_cleanup_loop, daemon=True
        )
        self.game_cleanup_thread.start()


    def api_server_accept(self):
        while True:
            try:
                raw, _ = self.listener.accept()
            except OSError as error:
                print(f"[SERVER] Accept failed: {error}")
                continue
            threading.Thread(
                target=self.api_connection, args=(raw,), daemon=True
            ).start()
    
    def recv_exact(self, c, length):
        data = bytearray()
        while len(data) < length:
            chunk = c.recv(length - len(data))
            if not chunk:
                raise ConnectionError("Client disconnected while sending a request")
            data.extend(chunk)
        return bytes(data)

    def send_json_message(self, c, message):
        payload = json.dumps(message).encode("utf-8")
        if not 1 <= len(payload) <= MAX_FRAME:
            raise ValueError("Invalid response length")
        c.sendall(struct.pack("!I", len(payload)) + payload)

    def api_connection(self, raw):
        try:
            raw.settimeout(10)
            c = self.tls_context.wrap_socket(raw, server_side=True)
        except (ssl.SSLError, OSError) as error:
            print(f"[SERVER] TLS handshake failed: {error}")
            raw.close()
            return
        with c:
            try:
                c.settimeout(30)
                header_length = struct.unpack("!I", self.recv_exact(c, 4))[0]
                if header_length == 0:
                    self.send_json_message(
                        c, {"ok": False, "error": "Invalid request frame"}
                    )
                    return
                if header_length > MAX_FRAME:
                    self.send_json_message(
                        c, {"ok": False, "error": "Request frame is too large"}
                    )
                    return
                request = json.loads(self.recv_exact(c, header_length))
                if not isinstance(request, dict):
                    self.send_json_message(c, {"ok": False, "error": "Invalid request"})
                    return

                version = request.get("v")
                if (
                    not isinstance(version, int)
                    or isinstance(version, bool)
                    or version != CLIENT_VERSION
                ):
                    self.send_json_message(
                        c, {"ok": False, "error": CLIENT_UPDATE_MESSAGE}
                    )
                    return

                if (
                    not isinstance(request.get("type"), str)
                    or not isinstance(request.get("data"), dict)
                ):
                    self.send_json_message(c, {"ok": False, "error": "Invalid request"})
                    return

                action = request["type"]
                if action not in self.request_fields:
                    self.send_json_message(
                        c, {"ok": False, "error": "Unknown request type"}
                    )
                    return
                self.validate_request_data(action, request["data"])

                if action not in {"register", "login"} and not isinstance(
                    request.get("token"), str
                ):
                    self.send_json_message(
                        c, {"ok": False, "error": "Authentication required"}
                    )
                    return

                if action in {"register", "login"}:
                    response = (
                        self.auth_register(request["data"])
                        if action == "register"
                        else self.auth_login(request["data"])
                    )
                else:
                    session_token = request["token"]
                    user_id = self.session_user_id(session_token)
                    if user_id is None:
                        response = {"ok": False, "error": "Authentication required"}
                    elif action == "logout":
                        self.logout_session(session_token)
                        response = {
                            "ok": True,
                            "data": {"status": "logged_out"},
                        }
                    else:
                        result = self.api_dispatch(
                            action, user_id, request["data"]
                        )
                        response = {"ok": True, "data": result}
                self.send_json_message(c, response)
            except (ValueError, UnicodeDecodeError) as error:
                self.send_json_message(
                    c, {"ok": False, "error": str(error)}
                )
            except sqlite3.Error as error:
                print(f"[SERVER] API database error: {error}")
                self.send_json_message(
                    c, {"ok": False, "error": "Database operation failed"}
                )
            except OSError as error:
                print(f"[SERVER] API connection error: {error}")
            except Exception as error:
                print(f"[SERVER] Unexpected API error: {error}")
                try:
                    self.send_json_message(
                        c, {"ok": False, "error": "Internal server error"}
                    )
                except OSError as send_error:
                    print(f"[SERVER] Could not send error reply: {send_error}")

    request_fields = {
        "register": {"username": str, "password": str},
        "login": {"username": str, "password": str},
        "logout": {},
        "get_profile": {},
        "get_dashboard": {},
        "get_club": {},
        "get_squad": {},
        "set_squad_slot": {"slot": int, "name": str},
        "buy_pack": {"pack": int},
        "store_pack": {"cards": list},
        "quick_sell": {},
        "get_unassigned": {},
        "friends_list": {},
        "add_friend": {"username": str},
        "respond_request": {"username": str, "accept": bool},
        "remove_friend": {"username": str},
        "challenge_friend": {"username": str},
        "respond_challenge": {"username": str, "accept": bool},
        "hh_join": {"mode": str},
        "hh_state": {},
        "hh_play": {"card_id": int},
        "hh_leave": {},
    }

    @staticmethod
    def validate_request_data(action, data):
        expected_fields = server.request_fields[action]
        if data.keys() != expected_fields.keys():
            raise ValueError("Invalid request data fields")
        for field, expected_type in expected_fields.items():
            value = data[field]
            if not isinstance(value, expected_type) or (
                expected_type is int
                and isinstance(value, bool)
            ):
                raise ValueError(f"Invalid request data type for {field}")
        if action == "store_pack" and any(
            not isinstance(path, str) for path in data["cards"]
        ):
            raise ValueError("Invalid request data type for cards")

    def auth_register(self, data):
        username = data.get("username")
        password = data.get("password")
        if not isinstance(username, str) or not isinstance(password, str):
            return {"ok": False, "error": "Invalid username or password"}
        username = username.strip()
        if not username:
            return {"ok": False, "error": "No Username Entered"}
        if not 7 <= len(password) <= 128:
            return {"ok": False, "error": "Invalid Password"}

        with user_db() as conn:
            cur = conn.cursor()
            cur.execute("BEGIN IMMEDIATE")
            cur.execute(
                "SELECT 1 FROM userdatabase WHERE username = ? COLLATE NOCASE",
                (username,),
            )
            if cur.fetchone():
                return {"ok": False, "error": "Username Already Registered"}
            cur.execute(
                "INSERT INTO userdatabase (username, password, coinbalance) "
                "VALUES (?, ?, ?)",
                (username, hash_password(password), 10000),
            )
        return {"ok": True, "data": {"username": username}}

    def auth_login(self, data):
        username = data.get("username")
        password = data.get("password")
        if not isinstance(username, str) or not isinstance(password, str):
            return {"ok": False, "error": "Incorrect username or password."}

        with user_db() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, username, password FROM userdatabase "
                "WHERE username = ? COLLATE NOCASE",
                (username.strip(),),
            )
            row = cur.fetchone()
            if row:
                authenticated, upgrade = verify_password(password, row[2])
            else:
                verify_password(password, DUMMY_HASH)
                authenticated = upgrade = False

            if not authenticated:
                return {
                    "ok": False,
                    "error": "Incorrect username or password.",
                }
            if upgrade:
                cur.execute(
                    "UPDATE userdatabase SET password = ? WHERE id = ?",
                    (hash_password(password), row[0]),
                )

        session_token = secrets.token_urlsafe(32)
        with self.lock:
            self.sessions[session_token] = (
                row[0],
                time.time() + SESSION_TTL_SECONDS,
            )
        return {
            "ok": True,
            "data": {"username": row[1], "token": session_token},
        }

    def api_dispatch(self, action, user_id, data):
        handlers = {
            "get_profile": self.api_get_profile,
            "get_dashboard": self.api_get_dashboard,
            "get_club": self.api_get_club,
            "get_squad": self.api_get_squad,
            "set_squad_slot": self.api_set_squad_slot,
            "buy_pack": self.api_buy_pack,
            "store_pack": self.api_store_pack,
            "quick_sell": self.api_quick_sell,
            "get_unassigned": self.api_get_unassigned,
            "friends_list": self.api_friends_list,
            "add_friend": self.api_add_friend,
            "respond_request": self.api_respond_friend_request,
            "remove_friend": self.api_remove_friend,
            "challenge_friend": self.api_challenge_friend,
            "respond_challenge": self.api_respond_challenge,
            "hh_join": self.api_hh_join,
            "hh_state": self.api_hh_state,
            "hh_play": self.api_hh_play,
            "hh_leave": self.api_hh_leave,
        }
        handler = handlers.get(action)
        if handler is None:
            raise ValueError("Unknown request")
        return handler(user_id, data)

    def api_get_profile(self, user_id, data):
        with user_db() as conn:
            row = conn.execute(
                "SELECT wins, losses, draws, coinbalance FROM userdatabase WHERE id = ?",
                (user_id,),
            ).fetchone()
        if row is None:
            raise ValueError("Account was not found")
        return self.api_format_profile(row)

    @staticmethod
    def api_format_profile(row):
        wins, losses, draws, balance = row
        return {
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "coins": balance,
            "record_text": f"Record: {wins}W - {draws}D - {losses}L",
            "balance_text": f"Coin balance: {balance:,}",
        }

    @staticmethod
    def api_get_squad_slots(conn, user_id):
        attach_cards_db(conn)
        squad = {
            slot: (card_id, image, name)
            for slot, card_id, image, name in conn.execute(
                "SELECT active_squad.slot, active_squad.card_id, "
                "cards_db.all_cards.card_image_path, "
                "cards_db.all_cards.card_name "
                "FROM active_squad LEFT JOIN cards_db.all_cards "
                "ON cards_db.all_cards.id = active_squad.card_id "
                "WHERE active_squad.user_id = ?",
                (user_id,),
            )
        }
        return [
            {
                "id": squad.get(slot, (None, None, None))[0],
                "image": squad.get(slot, (None, None, None))[1],
                "name": squad.get(slot, (None, None, None))[2],
            }
            for slot in range(1, 6)
        ]

    def api_get_dashboard(self, user_id, data):
        with user_db() as conn:
            profile_row = conn.execute(
                "SELECT wins, losses, draws, coinbalance "
                "FROM userdatabase WHERE id = ?",
                (user_id,),
            ).fetchone()
            if profile_row is None:
                raise ValueError("Account was not found")
            slots = self.api_get_squad_slots(conn, user_id)
        return {
            "profile": self.api_format_profile(profile_row),
            "slots": slots,
        }

    def api_get_club(self, user_id, data):
        with user_db() as conn:
            attach_cards_db(conn)
            paths = [
                row[0]
                for row in conn.execute(
                    "SELECT cards_db.all_cards.card_image_path "
                    "FROM user_cards JOIN cards_db.all_cards "
                    "ON cards_db.all_cards.id = user_cards.card_id "
                    "WHERE user_cards.user_id = ? ORDER BY user_cards.id",
                    (user_id,),
                )
            ]
        return {"cards": paths}

    def api_get_squad(self, user_id, data):
        with user_db() as conn:
            slots = self.api_get_squad_slots(conn, user_id)
        return {"slots": slots}

    def api_set_squad_slot(self, user_id, data):
        slot = data.get("slot")
        value = data.get("name")
        if not isinstance(slot, int) or isinstance(slot, bool) or not 1 <= slot <= 5:
            raise ValueError("Squad slot must be between 1 and 5")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("No Name Entered")
        normalized_input = normalize_card_search(value.strip())
        with user_db() as conn:
            attach_cards_db(conn)
            owned_cards = conn.execute(
                "SELECT cards_db.all_cards.id, cards_db.all_cards.card_name, "
                "cards_db.all_cards.card_image_path FROM user_cards "
                "JOIN cards_db.all_cards ON cards_db.all_cards.id = user_cards.card_id "
                "WHERE user_cards.user_id = ?",
                (user_id,),
            ).fetchall()
            matched = next(
                (
                    card
                    for card in owned_cards
                    if normalized_input in normalize_card_search(card[1])
                ),
                None,
            )
            if matched is None:
                raise ValueError("Cannot add a player not currently your club")
            card_id = matched[0]
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute(
                    "INSERT INTO active_squad (user_id, slot, card_id) VALUES (?, ?, ?) "
                    "ON CONFLICT(user_id, slot) DO UPDATE SET card_id = excluded.card_id",
                    (user_id, slot, card_id),
                )
            except sqlite3.IntegrityError as error:
                if "active_squad.user_id, active_squad.card_id" in str(error):
                    raise ValueError("Player already in active squad") from error
                raise
        return self.api_get_squad(user_id, {})

    def api_buy_pack(self, user_id, data):
        cost = data.get("pack")
        count = PACKS.get(cost) if isinstance(cost, int) and not isinstance(cost, bool) else None
        if count is None:
            raise ValueError("Invalid pack")
        with sqlite3.connect(CARDS_DATABASE_PATH) as cards_conn:
            cards = cards_conn.execute(
                "SELECT id, card_image_path FROM all_cards ORDER BY id"
            ).fetchall()
        if len(cards) < count:
            raise ValueError("Not enough cards are available")
        selected_cards = random.sample(cards, k=count)
        paths = [row[1] for row in selected_cards]
        with user_db() as conn:
            conn.execute("BEGIN IMMEDIATE")
            changed = conn.execute(
                "UPDATE userdatabase SET coinbalance = coinbalance - ? "
                "WHERE id = ? AND coinbalance >= ?",
                (cost, user_id, cost),
            ).rowcount
            if changed != 1:
                raise ValueError("Not enough coins")
            conn.executemany(
                "INSERT INTO unassigned_items (user_id, card_id) VALUES (?, ?)",
                [(user_id, card[0]) for card in selected_cards],
            )
        return {"cards": paths, "coins": self.api_get_profile(user_id, {})["coins"]}

    def api_get_unassigned(self, user_id, data):
        with user_db() as conn:
            attach_cards_db(conn)
            rows = conn.execute(
                "SELECT cards_db.all_cards.card_image_path FROM unassigned_items "
                "JOIN cards_db.all_cards ON cards_db.all_cards.id = unassigned_items.card_id "
                "WHERE unassigned_items.user_id = ? ORDER BY unassigned_items.id",
                (user_id,),
            ).fetchall()
        return {"cards": [row[0] for row in rows]}

    def api_store_pack(self, user_id, data):
        paths = data.get("cards")
        if (
            not isinstance(paths, list)
            or not paths
            or any(not isinstance(path, str) for path in paths)
        ):
            raise ValueError("Invalid pack card list")
        with user_db() as conn:
            attach_cards_db(conn)
            conn.execute("BEGIN IMMEDIATE")
            rows = conn.execute(
                "SELECT unassigned_items.id, cards_db.all_cards.id, "
                "cards_db.all_cards.card_image_path FROM unassigned_items "
                "JOIN cards_db.all_cards ON cards_db.all_cards.id = unassigned_items.card_id "
                "WHERE unassigned_items.user_id = ? ORDER BY unassigned_items.id",
                (user_id,),
            ).fetchall()
            selected = []
            remaining = list(paths)
            for item_id, card_id, path in rows:
                if path in remaining:
                    selected.append((item_id, card_id, path))
                    remaining.remove(path)
            if remaining:
                raise ValueError("Pack contains cards that are not unassigned")
            duplicates = []
            for item_id, card_id, path in selected:
                owned = conn.execute(
                    "SELECT 1 FROM user_cards WHERE user_id = ? AND card_id = ?",
                    (user_id, card_id),
                ).fetchone()
                conn.execute(
                    "DELETE FROM unassigned_items WHERE id = ? AND user_id = ?",
                    (item_id, user_id),
                )
                if owned:
                    conn.execute(
                        "INSERT INTO unassigned_items (user_id, card_id) "
                        "VALUES (?, ?)",
                        (user_id, card_id),
                    )
                    duplicates.append(path)
                else:
                    conn.execute(
                        "INSERT INTO user_cards (user_id, card_id) VALUES (?, ?)",
                        (user_id, card_id),
                    )
        return {"duplicates": duplicates, "stored": len(selected) - len(duplicates)}

    def api_quick_sell(self, user_id, data):
        with user_db() as conn:
            attach_cards_db(conn)
            conn.execute("BEGIN IMMEDIATE")
            rows = conn.execute(
                "SELECT unassigned_items.id, unassigned_items.card_id "
                "FROM unassigned_items WHERE user_id = ?",
                (user_id,),
            ).fetchall()
            sold_ids = []
            for item_id, card_id in rows:
                if conn.execute(
                    "SELECT 1 FROM user_cards WHERE user_id = ? AND card_id = ?",
                    (user_id, card_id),
                ).fetchone():
                    sold_ids.append(item_id)
            conn.executemany(
                "DELETE FROM unassigned_items WHERE id = ? AND user_id = ?",
                [(item_id, user_id) for item_id in sold_ids],
            )
            coins = len(sold_ids) * QUICK_SELL_VALUE
            conn.execute(
                "UPDATE userdatabase SET coinbalance = coinbalance + ? WHERE id = ?",
                (coins, user_id),
            )
        return {"sold": len(sold_ids), "coins_added": coins}

    def api_friends_list(self, user_id, data):
        with user_db() as conn:
            friends = [
                row[0]
                for row in conn.execute(
                    "SELECT friend.username FROM friends_list "
                    "JOIN userdatabase AS friend ON friend.id = friends_list.friend_id "
                    "WHERE friends_list.user_id = ? ORDER BY friend.username",
                    (user_id,),
                )
            ]
            requests = [
                row[0]
                for row in conn.execute(
                    "SELECT sender.username FROM incoming_friend_requests "
                    "JOIN userdatabase AS sender "
                    "ON sender.id = incoming_friend_requests.from_user_id "
                    "WHERE incoming_friend_requests.user_id = ? "
                    "ORDER BY sender.username",
                    (user_id,),
                )
            ]
            challenges = [
                row[0]
                for row in conn.execute(
                    "SELECT sender.username FROM incoming_challenge_requests "
                    "JOIN userdatabase AS sender "
                    "ON sender.id = incoming_challenge_requests.from_user_id "
                    "WHERE incoming_challenge_requests.user_id = ? "
                    "ORDER BY sender.username",
                    (user_id,),
                )
            ]
        return {
            "friends": friends,
            "friend_requests": requests,
            "challenge_requests": challenges,
        }

    def api_add_friend(self, user_id, data):
        name = data.get("username")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("No Name Was Entered")
        name = name.strip()
        with user_db() as conn:
            target = conn.execute(
                "SELECT id FROM userdatabase WHERE username = ? COLLATE NOCASE",
                (name,),
            ).fetchone()
            if target is None:
                raise ValueError("User doesn't exist")
            friend_id = target[0]
            if friend_id == user_id:
                raise ValueError("Cannot add yourself")
            conn.execute("BEGIN IMMEDIATE")
            if conn.execute(
                "SELECT 1 FROM friends_list WHERE user_id = ? AND friend_id = ?",
                (user_id, friend_id),
            ).fetchone():
                raise ValueError("User already added")
            if conn.execute(
                "SELECT 1 FROM incoming_friend_requests "
                "WHERE user_id = ? AND from_user_id = ?",
                (friend_id, user_id),
            ).fetchone():
                raise ValueError("Already sent a friend request")
            conn.execute(
                "INSERT INTO incoming_friend_requests (user_id, from_user_id) "
                "VALUES (?, ?)",
                (friend_id, user_id),
            )
        return {"status": "Sent friend request to user"}

    def api_respond_friend_request(self, user_id, data):
        name = data.get("username")
        accept = data.get("accept")
        if not isinstance(name, str) or not isinstance(accept, bool):
            raise ValueError("Invalid friend request response")
        with user_db() as conn:
            conn.execute("BEGIN IMMEDIATE")
            sender = conn.execute(
                "SELECT sender.id FROM incoming_friend_requests AS request "
                "JOIN userdatabase AS sender ON sender.id = request.from_user_id "
                "WHERE request.user_id = ? AND sender.username = ? COLLATE NOCASE",
                (user_id, name),
            ).fetchone()
            if sender is None:
                raise ValueError("Friend request is no longer available")
            conn.execute(
                "DELETE FROM incoming_friend_requests "
                "WHERE user_id = ? AND from_user_id = ?",
                (user_id, sender[0]),
            )
            if accept:
                conn.executemany(
                    "INSERT OR IGNORE INTO friends_list (user_id, friend_id) "
                    "VALUES (?, ?)",
                    ((user_id, sender[0]), (sender[0], user_id)),
                )
        return {"status": "Done"}

    def api_remove_friend(self, user_id, data):
        name = data.get("username")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid friend name")
        with user_db() as conn:
            other = conn.execute(
                "SELECT id FROM userdatabase WHERE username = ? COLLATE NOCASE",
                (name.strip(),),
            ).fetchone()
            if other is None:
                raise ValueError("Friend was not found")
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                "DELETE FROM friends_list WHERE user_id = ? AND friend_id = ?",
                (user_id, other[0]),
            )
            conn.execute(
                "DELETE FROM friends_list WHERE user_id = ? AND friend_id = ?",
                (other[0], user_id),
            )
        return {"status": "Done"}

    def api_challenge_friend(self, user_id, data):
        name = data.get("username")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid friend name")
        name = name.strip()
        squad = self.api_get_squad(user_id, {})["slots"]
        if any(not slot["id"] for slot in squad):
            raise ValueError("You do not have enough players in your active squad")
        with user_db() as conn:
            target = conn.execute(
                "SELECT target.id FROM userdatabase AS target "
                "JOIN friends_list AS friendship ON friendship.friend_id = target.id "
                "WHERE friendship.user_id = ? AND target.username = ? COLLATE NOCASE",
                (user_id, name),
            ).fetchone()
        if target is None:
            raise ValueError("Challenge target is not your friend")
        with self.lock:
            if user_id in self.api_player_games:
                raise ValueError("You are already in a game")
            if target[0] in self.api_player_games:
                raise ValueError("That player is already in a game")
            game_id = self.api_next_game_id
            self.api_next_game_id += 1
            meta = self.api_new_game_meta("challenge")
            meta["squads"][0] = self.api_load_game_squad(user_id)
            meta["last_seen"][0] = time.monotonic()
            self.api_game_meta[game_id] = meta
            self.game_accounts[game_id] = {0: user_id}
            self.api_player_games[user_id] = (game_id, 0)
        try:
            with user_db() as conn:
                conn.execute("BEGIN IMMEDIATE")
                conn.execute(
                    "INSERT INTO incoming_challenge_requests "
                    "(user_id, from_user_id, game_id) VALUES (?, ?, ?)",
                    (target[0], user_id, game_id),
                )
        except sqlite3.Error:
            with self.lock:
                self.api_player_games.pop(user_id, None)
                self.api_game_meta.pop(game_id, None)
                self.game_accounts.pop(game_id, None)
            raise
        return {"status": "Done"}

    def api_respond_challenge(self, user_id, data):
        name = data.get("username")
        accept = data.get("accept")
        if not isinstance(name, str) or not isinstance(accept, bool):
            raise ValueError("Invalid challenge response")
        accepted_squad = self.api_load_game_squad(user_id) if accept else None
        with self.lock:
            if accept and user_id in self.api_player_games:
                raise ValueError("You are already in a game")
            with user_db() as conn:
                conn.execute("BEGIN IMMEDIATE")
                row = conn.execute(
                    "SELECT request.game_id, sender.id "
                    "FROM incoming_challenge_requests AS request "
                    "JOIN userdatabase AS sender ON sender.id = request.from_user_id "
                    "WHERE request.user_id = ? AND sender.username = ? COLLATE NOCASE",
                    (user_id, name),
                ).fetchone()
                if row is None:
                    raise ValueError("Challenge request is no longer available")
                game_id, challenger_id = row
            meta = self.api_game_meta.get(game_id)
            accounts = self.game_accounts.get(game_id)
            if meta is None or accounts is None or accounts.get(0) != challenger_id:
                raise ValueError("Challenge has expired")
            if accept and (meta["phase"] != "waiting" or 1 in accounts):
                raise ValueError("Challenge is no longer available")
            with user_db() as conn:
                conn.execute(
                    "DELETE FROM incoming_challenge_requests "
                    "WHERE user_id = ? AND from_user_id = ?",
                    (user_id, challenger_id),
                )
            if not accept:
                meta["phase"] = "finished"
                meta["finished_at"] = time.monotonic()
                meta["result"] = "challenge_declined"
                return {"status": "Done"}
            accounts[1] = user_id
            meta["squads"][1] = accepted_squad
            now = time.monotonic()
            meta["last_seen"][1] = now
            meta["last_activity"] = now
            meta["phase"] = "playing"
            self.api_player_games[user_id] = (game_id, 1)
        return {"status": "Done"}

    def api_hh_join(self, user_id, data):
        mode = data.get("mode", "random")
        if mode not in ("random", "challenge"):
            raise ValueError("Invalid game mode")
        with self.lock:
            session = self.api_player_games.get(user_id)
            if session is not None:
                game_id, player = session
                meta = self.api_game_meta.get(game_id)
                if meta is None or meta["phase"] == "finished":
                    self.api_player_games.pop(user_id, None)
                    session = None
                elif meta["mode"] != mode:
                    raise ValueError("You are already in a different game")
            if session is None and mode == "challenge":
                raise ValueError("No accepted challenge is available")
            elif session is None:
                game_id = self.api_waiting_game
                if (
                    game_id is not None
                    and game_id in self.api_game_meta
                    and self.api_game_meta[game_id]["phase"] == "waiting"
                    and 1 not in self.game_accounts[game_id]
                    and time.monotonic()
                    - self.api_game_meta[game_id]["last_seen"].get(0, 0)
                    <= 20
                ):
                    accounts = self.game_accounts[game_id]
                    if accounts.get(0) == user_id:
                        raise ValueError("You are already waiting for a game")
                    player = 1
                    accounts[player] = user_id
                    meta = self.api_game_meta[game_id]
                    meta["squads"][1] = self.api_load_game_squad(user_id)
                    now = time.monotonic()
                    meta["last_seen"][1] = now
                    meta["last_activity"] = now
                    meta["phase"] = "playing"
                    self.api_waiting_game = None
                else:
                    stale_game_id = game_id
                    if (
                        stale_game_id in self.api_game_meta
                        and self.api_game_meta[stale_game_id]["phase"] == "waiting"
                    ):
                        stale_user = self.game_accounts.get(
                            stale_game_id, {}
                        ).get(0)
                        if stale_user is not None:
                            self.api_player_games.pop(stale_user, None)
                        self.api_game_meta.pop(stale_game_id, None)
                        self.game_accounts.pop(stale_game_id, None)
                    self.api_waiting_game = None
                    game_id = None
                if game_id is None:
                    game_id = self.api_next_game_id
                    self.api_next_game_id += 1
                    player = 0
                    meta = self.api_new_game_meta("random")
                    meta["squads"][0] = self.api_load_game_squad(user_id)
                    now = time.monotonic()
                    meta["last_seen"][0] = now
                    meta["last_activity"] = now
                    self.api_game_meta[game_id] = meta
                    self.game_accounts[game_id] = {0: user_id}
                    self.api_waiting_game = game_id
                    self.api_player_games[user_id] = (game_id, player)
            meta = self.api_game_meta[game_id]
            now = time.monotonic()
            meta["last_seen"][player] = now
            meta["last_activity"] = now
            self.api_player_games[user_id] = (game_id, player)
        return {"game_id": game_id, "player": player, "state": self.api_game_state(user_id)}

    def api_new_game_meta(self, mode):
        return {
            "mode": mode,
            "phase": "waiting",
            "round": 1,
            "stat": secrets.choice(tuple(GAME_STATS)),
            "squads": {0: [], 1: []},
            "played": {0: None, 1: None},
            "wins": [0, 0],
            "draws": 0,
            "last_round": None,
            "round_over_at": None,
            "last_seen": {},
            "last_activity": time.monotonic(),
            "finished_at": None,
            "settled": False,
            "forfeit_winner": None,
        }

    def api_load_game_squad(self, user_id):
        squad = self.api_get_squad(user_id, {})["slots"]
        if any(not slot["id"] for slot in squad):
            raise ValueError("You do not have enough players in your active squad")
        return [
            {
                "id": slot["id"],
                "name": slot["name"],
                "image": slot["image"],
                "used": False,
            }
            for slot in squad
        ]

    def api_game_state(self, user_id):
        with self.lock:
            session = self.api_player_games.get(user_id)
            if session is None:
                raise ValueError("Not connected to a game")
            game_id, player = session
            meta = self.api_game_meta.get(game_id)
            if meta is None:
                raise ValueError("Game is no longer available")
            now = time.monotonic()
            meta["last_seen"][player] = now
            meta["last_activity"] = now
            accounts = self.game_accounts.get(game_id, {})
            opponent = 1 - player
            if (
                meta["phase"] == "round_over"
                and meta["round_over_at"] is not None
                and now >= meta["round_over_at"]
            ):
                if meta["round"] == 5:
                    meta["phase"] = "finished"
                    meta["finished_at"] = now
                    self.api_settle_game(game_id)
                else:
                    meta["round"] += 1
                    meta["stat"] = secrets.choice(tuple(GAME_STATS))
                    meta["played"] = {0: None, 1: None}
                    meta["phase"] = "playing"
                    meta["round_over_at"] = None
            if (
                opponent in accounts
                and meta["phase"] != "finished"
                and now - meta["last_seen"].get(opponent, now) > 20
            ):
                meta["phase"] = "finished"
                meta["finished_at"] = now
                meta["forfeit_winner"] = player
                meta["result"] = "forfeit"
                self.api_settle_disconnect(game_id, player)

            last_round = None
            if meta["last_round"] is not None and meta["phase"] in (
                "round_over", "finished"
            ):
                result = meta["last_round"]
                last_round = {
                    "my_card": result["cards"][player]["id"],
                    "opp_card": result["cards"][opponent]["id"],
                    "my_value": result["values"][player],
                    "opp_value": result["values"][opponent],
                    "winner": (
                        "draw" if result["winner"] == -1
                        else "me" if result["winner"] == player
                        else "opponent"
                    ),
                    "my_image": result["cards"][player]["image"],
                    "opp_image": result["cards"][opponent]["image"],
                }
            finished_result = None
            if meta["phase"] == "finished":
                if meta.get("result") == "challenge_declined":
                    finished_result = "challenge_declined"
                elif meta.get("forfeit_winner") is not None:
                    finished_result = (
                        "forfeit_win" if meta["forfeit_winner"] == player
                        else "forfeit_loss"
                    )
                elif meta["wins"][player] > meta["wins"][opponent]:
                    finished_result = "win"
                elif meta["wins"][player] < meta["wins"][opponent]:
                    finished_result = "loss"
                else:
                    finished_result = "draw"
            return {
                "phase": meta["phase"],
                "round": meta["round"],
                "stat": meta["stat"],
                "my_cards": [
                    {"id": card["id"], "used": card["used"]}
                    for card in meta["squads"][player]
                ],
                "i_played": meta["played"][player] is not None,
                "opponent_played": meta["played"][opponent] is not None,
                "last_round": last_round,
                "result": finished_result,
                "wins": meta["wins"][player],
                "opponent_wins": meta["wins"][opponent],
                "draws": meta["draws"],
            }

    def api_hh_state(self, user_id, data):
        return self.api_game_state(user_id)

    def api_hh_play(self, user_id, data):
        card_id = data.get("card_id")
        if not isinstance(card_id, int) or isinstance(card_id, bool):
            raise ValueError("Invalid card selection")
        with self.lock:
            session = self.api_player_games.get(user_id)
            if session is None:
                raise ValueError("Not connected to a game")
            game_id, player = session
            meta = self.api_game_meta[game_id]
            if meta["phase"] != "playing":
                raise ValueError("The game is not accepting a card right now")
            if 1 not in self.game_accounts.get(game_id, {}):
                raise ValueError("Waiting for another player")
            if meta["played"][player] is not None:
                raise ValueError("Turn is already locked")
            card = next(
                (item for item in meta["squads"][player] if item["id"] == card_id),
                None,
            )
            if card is None or card["used"]:
                raise ValueError("Selected card is not available")
            stat_column = GAME_STATS[meta["stat"]]
            with sqlite3.connect(CARDS_DATABASE_PATH) as conn:
                row = conn.execute(
                    f"SELECT {stat_column} FROM all_cards WHERE id = ?",
                    (card_id,),
                ).fetchone()
            if row is None:
                raise ValueError("Selected card data was not found")
            card["used"] = True
            meta["played"][player] = {"id": card_id, "value": row[0]}
            meta["last_activity"] = time.monotonic()
            if meta["played"][0] is not None and meta["played"][1] is not None:
                values = {
                    0: meta["played"][0]["value"],
                    1: meta["played"][1]["value"],
                }
                if values[0] > values[1]:
                    winner = 0
                    meta["wins"][0] += 1
                elif values[1] > values[0]:
                    winner = 1
                    meta["wins"][1] += 1
                else:
                    winner = -1
                    meta["draws"] += 1
                cards = {
                    side: next(
                        item for item in meta["squads"][side]
                        if item["id"] == meta["played"][side]["id"]
                    )
                    for side in (0, 1)
                }
                meta["last_round"] = {
                    "cards": cards,
                    "values": values,
                    "winner": winner,
                }
                meta["phase"] = "round_over"
                meta["round_over_at"] = time.monotonic() + 3
        return self.api_game_state(user_id)

    def api_settle_game(self, game_id):
        meta = self.api_game_meta.get(game_id)
        accounts = self.game_accounts.get(game_id, {})
        if meta is None or meta["settled"] or 0 not in accounts or 1 not in accounts:
            return
        if meta["wins"][0] > meta["wins"][1]:
            results = {0: ("wins", 5000), 1: ("losses", 1000)}
        elif meta["wins"][1] > meta["wins"][0]:
            results = {0: ("losses", 1000), 1: ("wins", 5000)}
        else:
            results = {0: ("draws", 2500), 1: ("draws", 2500)}
        with user_db() as conn:
            conn.execute("BEGIN IMMEDIATE")
            for player, (column, coins) in results.items():
                conn.execute(
                    f"UPDATE userdatabase SET {column} = {column} + 1, "
                    "coinbalance = coinbalance + ? WHERE id = ?",
                    (coins, accounts[player]),
                )
        meta["settled"] = True

    def api_settle_disconnect(self, game_id, remaining_player):
        meta = self.api_game_meta.get(game_id)
        accounts = self.game_accounts.get(game_id, {})
        if meta is None or meta["settled"] or remaining_player not in accounts:
            return
        opponent = 1 - remaining_player
        if opponent not in accounts:
            return
        with user_db() as conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute(
                "UPDATE userdatabase SET wins = wins + 1, "
                "coinbalance = coinbalance + 5000 WHERE id = ?",
                (accounts[remaining_player],),
            )
            conn.execute(
                "UPDATE userdatabase SET losses = losses + 1, "
                "coinbalance = coinbalance + 1000 WHERE id = ?",
                (accounts[opponent],),
            )
        meta["settled"] = True
        meta["forfeit_winner"] = remaining_player

    def api_hh_leave(self, user_id, data):
        with self.lock:
            session = self.api_player_games.pop(user_id, None)
            if session is None:
                return {"status": "left"}
            game_id, player = session
            meta = self.api_game_meta.get(game_id)
            accounts = self.game_accounts.get(game_id, {})
            if meta is not None and meta["phase"] != "finished":
                if 1 in accounts:
                    meta["phase"] = "finished"
                    meta["finished_at"] = time.monotonic()
                    meta["forfeit_winner"] = 1 - player
                    self.api_settle_disconnect(game_id, 1 - player)
                else:
                    if meta["mode"] == "challenge":
                        with user_db() as conn:
                            conn.execute(
                                "DELETE FROM incoming_challenge_requests "
                                "WHERE game_id = ?",
                                (game_id,),
                            )
                    self.api_game_meta.pop(game_id, None)
                    self.game_accounts.pop(game_id, None)
            elif meta is not None and 1 not in accounts:
                self.api_game_meta.pop(game_id, None)
                self.game_accounts.pop(game_id, None)
            if self.api_waiting_game == game_id:
                self.api_waiting_game = None
            return {"status": "left"}

    def api_game_cleanup_loop(self):
        while True:
            time.sleep(GAME_CLEANUP_INTERVAL_SECONDS)
            try:
                removed = self.api_cleanup_games()
                if removed:
                    print(f"[SERVER] Cleaned up {removed} inactive game(s)")
            except Exception as error:
                print(f"[SERVER] Game cleanup failed: {error}")

    def api_cleanup_games(self):
        now = time.monotonic()
        with self.lock:
            stale_game_ids = []
            for game_id, meta in self.api_game_meta.items():
                last_activity = meta.get(
                    "last_activity",
                    max(meta.get("last_seen", {}).values(), default=now),
                )
                if meta["phase"] == "finished":
                    finished_at = meta.get("finished_at")
                    if finished_at is None:
                        finished_at = last_activity
                    is_stale = now - finished_at >= GAME_IDLE_TTL_SECONDS
                else:
                    is_stale = now - last_activity >= GAME_IDLE_TTL_SECONDS
                if is_stale:
                    stale_game_ids.append(game_id)

            if not stale_game_ids:
                return 0

            for game_id in stale_game_ids:
                for user_id, session in list(self.api_player_games.items()):
                    if session[0] == game_id:
                        del self.api_player_games[user_id]
                self.api_game_meta.pop(game_id, None)
                self.game_accounts.pop(game_id, None)
                if self.api_waiting_game == game_id:
                    self.api_waiting_game = None

            try:
                with user_db() as conn:
                    conn.executemany(
                        "DELETE FROM incoming_challenge_requests WHERE game_id = ?",
                        [(game_id,) for game_id in stale_game_ids],
                    )
            except sqlite3.Error as error:
                print(f"[SERVER] Could not clean expired challenge requests: {error}")

            return len(stale_game_ids)

    def session_user_id(self, session_token):
        now = time.time()
        with self.lock:
            expired_tokens = [
                token
                for token, (_, expires) in self.sessions.items()
                if expires <= now
            ]
            for token in expired_tokens:
                del self.sessions[token]
            session = self.sessions.get(session_token)
            return session[0] if session is not None else None

    def logout_session(self, session_token):
        with self.lock:
            self.sessions.pop(session_token, None)

if __name__ == "__main__":
    ServerSystem = server()
    ServerSystem.start()