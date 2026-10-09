import socket

from PyQt5 import QtWidgets

from Config.config import HOST, PORT
from Login.login_window_ui import Ui_MainWindow
from Server.protocol import recv_msg, send_msg
from Server.tls import create_client_context


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.login_button.clicked.connect(self.login)
        self.ui.signup_button.clicked.connect(self.show_signup)
        self.ui.register_button.clicked.connect(self.register)
        self.ui.already_registered_button.clicked.connect(self.show_login)
        self.ui.show_password_button.toggled.connect(self.toggle_login_password)
        self.ui.show_password_button_signup.toggled.connect(
            self.toggle_signup_password
        )

    def show_signup(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.register_page)

    def show_login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.login_page)

    def toggle_login_password(self, visible):
        echo_mode = (
            QtWidgets.QLineEdit.Normal if visible else QtWidgets.QLineEdit.Password
        )
        self.ui.password_textbox.setEchoMode(echo_mode)

    def toggle_signup_password(self, visible):
        echo_mode = (
            QtWidgets.QLineEdit.Normal if visible else QtWidgets.QLineEdit.Password
        )
        self.ui.password_textbox_signup.setEchoMode(echo_mode)
        self.ui.confirm_password_textbox.setEchoMode(echo_mode)

    def login(self):
        username = self.ui.username_textbox.text().strip()
        password = self.ui.password_textbox.text()
        if not username:
            QtWidgets.QMessageBox.warning(self, "Error", "No Username Entered")
            return
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "No Password Entered")
            return

        try:
            result = self._request("login", username, password)
        except (OSError, EOFError, ValueError, UnicodeDecodeError) as error:
            QtWidgets.QMessageBox.critical(self, "Connection Error", str(error))
            return

        if result["ok"]:
            self.navigator.session_token = result["data"]["token"]
            QtWidgets.QMessageBox.information(
                self, "Success", f"Welcome, {username}"
            )
            self.navigator.show_main()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", result["error"])

    def register(self):
        username = self.ui.username_textbox_signup.text().strip()
        password = self.ui.password_textbox_signup.text()
        confirm_password = self.ui.confirm_password_textbox.text()

        if not username:
            QtWidgets.QMessageBox.warning(self, "Error", "No Username Entered")
            return
        if not password:
            QtWidgets.QMessageBox.warning(self, "Error", "No Password Entered")
            return
        if len(password) < 7:
            QtWidgets.QMessageBox.warning(
                self, "Error", "Password is not long enough"
            )
            return
        if password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        try:
            result = self._request("register", username, password)
        except (OSError, EOFError, ValueError, UnicodeDecodeError) as error:
            QtWidgets.QMessageBox.critical(self, "Connection Error", str(error))
            return

        if result["ok"]:
            QtWidgets.QMessageBox.information(
                self, "Success", "User registered successfully"
            )
            self.ui.username_textbox.setText(username)
            self.show_login()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", result["error"])

    @staticmethod
    def _request(action, username, password):
        context = create_client_context()
        with socket.create_connection((HOST, PORT), timeout=10) as raw_socket:
            with context.wrap_socket(raw_socket, server_hostname=HOST) as client:
                send_msg(
                    client,
                    {
                        "v": 1,
                        "type": action,
                        "data": {"username": username, "password": password},
                    },
                )
                response = recv_msg(client)
        if not isinstance(response, dict) or not isinstance(response.get("ok"), bool):
            raise ValueError("Invalid authentication response")
        if response["ok"]:
            if not isinstance(response.get("data"), dict):
                raise ValueError("Invalid authentication response data")
            if action == "login" and not isinstance(
                response["data"].get("token"), str
            ):
                raise ValueError("Login response did not include a session token")
        elif not isinstance(response.get("error"), str):
            raise ValueError("Invalid authentication error response")
        return response

def main():
    from app import main as run_application

    run_application()


if __name__ == "__main__":
    main()
