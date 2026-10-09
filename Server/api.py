import socket
from Server.protocol import send_msg, recv_msg
from Server.tls import create_client_context
from Config.config import HOST, PORT

class ApiError(Exception):
    pass

class Api:
    def __init__(self, token=None):
        self.token = token

    def call(self, kind, **data):
        request = {"v": 1, "type": kind, "data": data}
        if self.token is not None:
            request["token"] = self.token
        context = create_client_context()
        with socket.create_connection((HOST, PORT), timeout=10) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname=HOST) as secure_socket:
                send_msg(secure_socket, request)
                reply = recv_msg(secure_socket)
        if not isinstance(reply, dict) or not isinstance(reply.get("ok"), bool):
            raise ApiError("Invalid API response")
        if not reply["ok"]:
            raise ApiError(str(reply.get("error", "API request failed")))
        if not isinstance(reply.get("data"), dict):
            raise ApiError("Invalid API response data")
        return reply["data"]