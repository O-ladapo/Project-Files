import json, struct

MAX_FRAME = 64 * 1024

def _recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed")
        buf += chunk
    return buf

def send_msg(sock, obj):
    data = json.dumps(obj).encode("utf-8")
    if not data or len(data) > MAX_FRAME:
        raise ValueError("message too large")
    sock.sendall(struct.pack(">I", len(data)) + data)

def recv_msg(sock):
    (length,) = struct.unpack(">I", _recv_exact(sock, 4))
    if not 1 <= length <= MAX_FRAME:
        raise ValueError("message too large")
    return json.loads(_recv_exact(sock, length).decode("utf-8"))