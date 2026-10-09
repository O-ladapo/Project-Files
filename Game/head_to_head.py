from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from Cards.paths import card_pixmap
from Game.head_to_head_ui import Ui_MainWindow
from Game.network import Network


class GameApiWorker(QThread):
    completed = pyqtSignal(object, str, object, object)

    def __init__(self, task_name, operation):
        super().__init__()
        self.task_name = task_name
        self.operation = operation

    def run(self):
        try:
            self.completed.emit(
                self, self.task_name, self.operation(), None
            )
        except Exception as error:
            self.completed.emit(self, self.task_name, None, error)


class MainWindow(QMainWindow):
    def __init__(self, nav, mode="random", session_token=None):
        super().__init__()
        self.nav = nav
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mode = mode
        self.player = 999
        self.cards_displayed = False
        self.card_info = []
        self.finished_handled = False
        self.disconnect_handled = False
        self.round_number = 0
        self.player1_points = 0
        self.player2_points = 0
        self.blank = QtGui.QPixmap(card_pixmap(""))
        self.n = None
        self._active_tasks = set()
        self._workers = set()
        self._closed = False

        self.player1_cards = self._make_card_labels("player1_card")
        self.player2_cards = self._make_card_labels("player2_card")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_data)
        self._run_game_task(
            "connect",
            lambda: Network(mode, session_token),
        )

    def _run_game_task(self, task_name, operation):
        if (self._closed and task_name != "leave") or task_name in self._active_tasks:
            return
        worker = GameApiWorker(task_name, operation)
        self._workers.add(worker)
        self._active_tasks.add(task_name)
        worker.completed.connect(self._handle_game_task_result)
        worker.finished.connect(
            lambda worker=worker: self._release_game_worker(worker)
        )
        worker.start()

    @pyqtSlot(object, str, object, object)
    def _handle_game_task_result(self, worker, task_name, result, error):
        self._active_tasks.discard(task_name)
        if self._closed:
            if task_name == "connect" and error is None and result.getP() != 999:
                self.n = result
                self._run_game_task("leave", self.n.leave_game)
            return
        if error is not None:
            print(f"[CLIENT] Head-to-head {task_name} failed: {error}")
            if task_name == "connect":
                QTimer.singleShot(0, self.nav.show_main)
            elif task_name == "state":
                self.handle_opponent_disconnect()
            return

        if task_name == "connect":
            self.n = result
            self.player = self.n.getP()
            if self.player == 999:
                QTimer.singleShot(0, self.nav.show_main)
                return
            self._run_game_task("cards", self.n.load_player_cards)
            self.timer.start(1000)
            self.show_data()
        elif task_name == "cards":
            self._display_my_cards(result)
        elif task_name == "state":
            if result is None:
                self.handle_opponent_disconnect()
            else:
                self.show_data(result)
        elif task_name == "play":
            if result is not None:
                self.show_data(result)

    def _release_game_worker(self, worker):
        self._workers.discard(worker)
        worker.deleteLater()

    def _make_card_labels(self, prefix):
        cards = {}
        for number in range(1, 6):
            original = self.findChild(QtWidgets.QLabel, f"{prefix}{number}")
            label = configureLabel(original.parent())
            label.setGeometry(original.geometry())
            label.setObjectName(original.objectName())
            label.show()
            original.hide()
            cards[number] = label
        return cards

    def show_data(self, state=None):
        if self.disconnect_handled or self._closed:
            return
        if state is None:
            if self.n is not None:
                self._run_game_task("state", self.n.get_state)
            return

        self.player1_points = state["wins"] if self.player == 0 else state["opponent_wins"]
        self.player2_points = state["opponent_wins"] if self.player == 0 else state["wins"]
        self.ui.player1_frame.setText(f"P1\n{self.player1_points}")
        self.ui.player2_frame.setText(f"P2\n{self.player2_points}")
        if state["phase"] != "waiting" and state["round"] != self.round_number:
            self.round_number = state["round"]
            self.display_stat(state["stat"])

        self.updateGUI(state)
        if state["phase"] == "round_over":
            last_round = state["last_round"]
            if last_round is not None:
                if last_round["winner"] == "draw":
                    text = "Tie Game!"
                elif last_round["winner"] == "me":
                    text = "You Won!"
                else:
                    text = "You Lost..."
                self.ui.winner_label.setText(text)
        elif state["phase"] == "waiting":
            self.ui.winner_label.setText("Waiting...")
        elif state["phase"] == "playing":
            self.ui.winner_label.setText(
                "Waiting for opponent..." if state["i_played"] else "Select a card"
            )
        elif state["phase"] == "finished":
            if state["result"] == "forfeit_win":
                self.handle_opponent_disconnect()
                return
            result_text = {
                "win": "You won the game!",
                "loss": "You lost the game.",
                "draw": "The game was a draw.",
                "forfeit_loss": "You lost because you disconnected.",
                "challenge_declined": "Your challenge was declined.",
            }
            self.display_finished_message(result_text[state["result"]])
            return

        own_cards = self.player1_cards if self.player == 0 else self.player2_cards
        for index, card_info in enumerate(self.card_info, start=1):
            status = next(
                (card for card in state["my_cards"] if card["id"] == card_info["id"]),
                None,
            )
            playable = (
                state["phase"] == "playing"
                and not state["i_played"]
                and status is not None
                and not status["used"]
            )
            if "play" in self._active_tasks:
                playable = False
            own_cards[index].setEnabled(playable)
            if playable and own_cards[index].clicked:
                own_cards[index].clicked = False
                own_cards[index].setEnabled(False)
                self._run_game_task(
                    "play",
                    lambda card_id=card_info["id"]: (
                        self.n.send_clicked_card(card_id)
                    ),
                )

    def _display_my_cards(self, cards):
        self.card_info = cards
        own_cards = self.player1_cards if self.player == 0 else self.player2_cards
        opponent_cards = self.player2_cards if self.player == 0 else self.player1_cards
        for index, info in enumerate(self.card_info, start=1):
            own_cards[index].setPixmap(card_pixmap(info["image"]))
            opponent_cards[index].setPixmap(self.blank)
            own_cards[index].setEnabled(False)
        self.cards_displayed = True

    def updateGUI(self, state):
        if state["phase"] in ("round_over", "finished") and state["last_round"]:
            last_round = state["last_round"]
            own_pixmap = QtGui.QPixmap(card_pixmap(last_round["my_image"]))
            opponent_pixmap = QtGui.QPixmap(card_pixmap(last_round["opp_image"]))
            if self.player == 0:
                self.ui.selected_card1.setPixmap(own_pixmap)
                self.ui.selected_card2.setPixmap(opponent_pixmap)
            else:
                self.ui.selected_card1.setPixmap(opponent_pixmap)
                self.ui.selected_card2.setPixmap(own_pixmap)
        else:
            self.ui.selected_card1.clear()
            self.ui.selected_card2.clear()

        if state["phase"] == "waiting":
            self.ui.winner_label.setText("Waiting for opponent...")

    def display_stat(self, stat):
        self.ui.game_type_label.setText(f"Stat Type: {stat}")
        attr_names = {
            "Pace": "example_pac",
            "Shooting": "example_sho",
            "Passing": "example_pas",
            "Dribbling": "example_dri",
            "Defending": "example_def",
            "Physical": "example_phy",
        }
        for attr, object_name in attr_names.items():
            label = getattr(self.ui, object_name)
            label.setStyleSheet(
                "background-color: None;\nborder: 2px solid black;"
                if attr == stat
                else "background-color: None;\nborder: 0px solid black;"
            )

    def display_finished_message(self, text):
        if self.finished_handled:
            return
        self.finished_handled = True
        self.timer.stop()
        message = QMessageBox(self)
        message.setWindowTitle("Game Over")
        message.setText(text)
        message.setIcon(QMessageBox.Information)
        message.setStandardButtons(QMessageBox.NoButton)
        message.show()
        QTimer.singleShot(3000, message.accept)
        QTimer.singleShot(3100, self.nav.show_main)

    def handle_opponent_disconnect(self):
        if self.disconnect_handled:
            return
        self.disconnect_handled = True
        self.timer.stop()
        message = QMessageBox(self)
        message.setWindowTitle("Opponent disconnected")
        message.setText("The other user has disconnected. You win!")
        message.setIcon(QMessageBox.Information)
        message.setStandardButtons(QMessageBox.NoButton)
        message.show()
        QTimer.singleShot(3000, message.accept)
        QTimer.singleShot(3100, self.nav.show_main)

    def closeEvent(self, event):
        self._closed = True
        self.timer.stop()
        if self.n is not None:
            self._run_game_task("leave", self.n.leave_game)
        if self.nav.current is self:
            self.nav.current = None
            self.nav.show_main()
        event.accept()


class configureLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicked = False
        self.setFixedSize(111, 141)
        self.setScaledContents(True)

    def mousePressEvent(self, event):
        if self.isEnabled():
            self.clicked = True
            self.setStyleSheet("background-color: rgb(25, 118, 210);")
        super().mousePressEvent(event)
