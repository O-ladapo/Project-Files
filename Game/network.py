from Server.api import Api, ApiError


def api_call(session_token, action, **data):
    return Api(session_token).call(action, **data)


class Network:
    def __init__(self, mode="random", session_token=None, disconnect_callback=None):
        self.session_token = session_token
        self.disconnect_callback = disconnect_callback
        self.disconnect_notified = False
        self.game_id = None
        self.player = self.connect(mode)

    def getP(self):
        return self.player

    def connect(self, mode):
        if not self.session_token:
            return 999
        try:
            result = api_call(self.session_token, "hh_join", mode=mode)
            self.game_id = result["game_id"]
            return result["player"]
        except (OSError, ValueError, ApiError) as error:
            print(f"[CLIENT] Connection failed: {error}")
            return 999

    def _notify_disconnect(self):
        if self.disconnect_notified:
            return
        self.disconnect_notified = True
        if self.disconnect_callback is not None:
            self.disconnect_callback()

    def get_state(self):
        try:
            state = api_call(self.session_token, "hh_state")
            if state.get("result") == "forfeit_win":
                self._notify_disconnect()
            return state
        except (OSError, ValueError, ApiError) as error:
            print(f"[CLIENT] Game state request failed: {error}")
            self._notify_disconnect()
            return None

    def send_clicked_card(self, card_id):
        try:
            state = api_call(self.session_token, "hh_play", card_id=card_id)
            if state.get("result") == "forfeit_win":
                self._notify_disconnect()
            return state
        except (OSError, ValueError, ApiError) as error:
            print(f"[CLIENT] Could not play card: {error}")
            return None

    def load_player_cards(self):
        try:
            return api_call(self.session_token, "get_squad")["slots"]
        except (OSError, ValueError, ApiError) as error:
            print(f"[CLIENT] Could not load squad: {error}")
            return []

    def leave_game(self):
        if self.game_id is None or self.session_token is None:
            return
        try:
            api_call(self.session_token, "hh_leave")
        except (OSError, ValueError, ApiError) as error:
            print(f"[CLIENT] Could not leave game cleanly: {error}")
        finally:
            self.game_id = None
