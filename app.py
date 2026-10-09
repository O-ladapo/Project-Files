import sys
from PyQt5.QtWidgets import QApplication

class Navigator:
    def __init__(self):
        self.current = None
        self.session_token = None

    def _swap(self, win):
        old, self.current = self.current, win
        win.show()
        if old is not None:
            old.close()

    def show_login(self):
        from Login.login import LoginWindow
        self._swap(LoginWindow(self))

    def show_main(self):
        from Game.main_game import MainWindow
        self._swap(MainWindow(self))

    def show_game(self, mode="random"):
        from Game.head_to_head import MainWindow as GameWindow
        self._swap(GameWindow(self, mode, self.session_token))


def main():
    application = QApplication(sys.argv)
    nav = Navigator()
    nav.show_login()
    return application.exec_()


if __name__ == "__main__":
    sys.exit(main())