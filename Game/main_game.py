from PyQt5 import QtWidgets #PyQt5 library functions
from PyQt5.QtCore import QObject, QThread, QTimer, pyqtSignal, pyqtSlot #Library which allows scheduling and triggering events within PyQt5
from PyQt5.QtWidgets import QMainWindow, QMessageBox #PyQt5 library functions
from Game.game_ui import Ui_MainWindow #Imports the menu GUI
from Game.pack_window_ui import Ui_PackWindow #Imports the pack GUI
from Game.how_to_play_ui import Ui_HelpWindow #Imports the how to play GUI
from Cards.paths import card_pixmap
from Game.network import api_call
from Server.api import ApiError


class ApiWorker(QThread):
    completed = pyqtSignal(object, str, object, object)

    def __init__(self, task_name, operation):
        super().__init__()
        self.owner = None
        self.task_name = task_name
        self.operation = operation

    def run(self):
        try:
            self.completed.emit(self, self.task_name, self.operation(), None)
        except Exception as error:
            self.completed.emit(self, self.task_name, None, error)


class MainWindow(QObject):
    def __init__(self, nav):
        super().__init__()
        self.nav = nav
        self._workers = set()
        self._active_tasks = set()
        self._closed = False
        self._club_cards_loaded = False
        self.main_win = QMainWindow() #Creates a variable which allows for the GUI class to be accessed
        self.ui = Ui_MainWindow() #Accesses the UI class from the game ui file
        self.ui.setupUi(self.main_win) #Sets up the GUI to be displayed

        self.pack_window = QtWidgets.QMainWindow() #Creates a variable which allows for the GUI class to be accessed
        self.pack = Ui_PackWindow() #Accesses the UI class from the pack window ui file
        self.pack.setupUi(self.pack_window) #Sets up the GUI to be displayed

        self.help_window = QtWidgets.QMainWindow() #Creates a variable which allows for the GUI class to be accessed
        self.help = Ui_HelpWindow() #Accesses the UI class from the how to play ui file
        self.help.setupUi(self.help_window) #Sets up the GUI to be displayed        
        
        self.ui.scrollAreaWidgetContents_club_layout = QtWidgets.QGridLayout(self.ui.scrollAreaWidgetContents_club) #Sets up the grid layout for the widget that stores the user cards
        self.pack.scrollAreaWidgetContents_show_packed_cards_layout = QtWidgets.QGridLayout(self.pack.scrollAreaWidgetContents_show_packed_cards) #Sets up the grid layout for showing cards in a pack
        
        self.ui.stacked_widget.setCurrentWidget(self.ui.homepage) #Sets the current widget to be the hompage. The first thing the user sees when logging in

        self.button_connect = button_connect(self) #Creates an instance of the button connect class
        self.club = club(self) #Creates an instance of the club class
        self.friends_list = friends_list(self) #Creates an instance of the friends list class
        self.store = store(self) #Creates an instance of the store class
        
        self.line_edits() #Calls the function which handles text inputs in the active squad
        self.buttons() #Calls the function which handles button action for the naviagtion bar and main homepage

    def request(self, action, **data):
        return api_call(self.nav.session_token, action, **data)

    def _run_api_task(self, task_name, operation):
        if self._closed or task_name in self._active_tasks:
            return
        worker = ApiWorker(task_name, operation)
        worker.owner = self
        self._workers.add(worker)
        self._active_tasks.add(task_name)
        worker.completed.connect(self._handle_api_result)
        worker.start()

    @pyqtSlot(object, str, object, object)
    def _handle_api_result(self, worker, task_name, result, error):
        self._active_tasks.discard(task_name)
        if self._closed:
            QTimer.singleShot(0, lambda: self._release_worker(worker))
            return
        try:
            if error is not None:
                if task_name == "refresh":
                    print(f"[CLIENT] Background refresh failed: {error}")
                else:
                    self.error_boxes(str(error))
                return

            if task_name == "initial_core":
                profile = result["profile"]
                slots = result["slots"]
                self.club.apply_account(profile)
                self.club.apply_active_squad(slots)
            elif task_name == "initial_aux":
                friends, unassigned = result
                self.friends_list.load_friends(friends)
                self.friends_list.show_incoming_friend_requests(friends)
                self.friends_list.show_incoming_challenge_requests(friends)
                self.store.check_unassigned(unassigned)
            elif task_name == "refresh":
                profile, friends = result
                self.club.apply_account(profile)
                self.friends_list.load_friends(friends)
                self.friends_list.show_incoming_friend_requests(friends)
                self.friends_list.show_incoming_challenge_requests(friends)
            elif task_name == "club":
                self.club.display_user_cards(result)
        finally:
            QTimer.singleShot(0, lambda: self._release_worker(worker))

    def _release_worker(self, worker):
        if worker.isFinished():
            self._workers.discard(worker)
            worker.owner = None
            return
        QTimer.singleShot(10, lambda: self._release_worker(worker))

    def refresh_account_data(self):
        if {"initial_core", "initial_aux"} & self._active_tasks:
            return
        self._run_api_task(
            "refresh",
            lambda: (
                self.request("get_profile"),
                self.request("friends_list"),
            ),
        )
        

    def buttons(self): #When each button is clicked, their various pages are displayed
        self.ui.main_page_button_nav.clicked.connect(self.button_connect.showHomepage) #Displays the homepage when clicked
        self.ui.club_button_nav.clicked.connect(self.button_connect.showClub) #Displays the club when clicked
        self.ui.transfer_market_button_nav.clicked.connect(self.button_connect.showTransfer_market) #Displays the transfer market when clicked
        self.ui.friends_list_button_nav.clicked.connect(self.button_connect.showFriends_list) #Displays the friends list when clicked
        self.ui.store_button_nav.clicked.connect(self.button_connect.showStore) #Displays the store when clicked
        self.ui.log_out_button_nav.clicked.connect(self.button_connect.loggedout) #Logs the user out of the application when clicked
        
        self.ui.friends_list_button.clicked.connect(self.button_connect.showFriends_list) #Displays the friends list when clicked
        self.ui.club_button.clicked.connect(self.button_connect.showClub) #Displays the club when clicked
        self.ui.store_button.clicked.connect(self.button_connect.showStore) #Displays the store when clicked
        self.ui.head_to_head_button.clicked.connect(self.button_connect.playGame) #Opens the head-to-head game when clicked

        self.ui.how_to_play_button.clicked.connect(self.button_connect.show_help) #Opens the how to play window when clicked
        self.help.club_button.clicked.connect(self.button_connect.show_club_help) #Opens the club section of the how to play window when clicked
        self.help.friends_list_button.clicked.connect(self.button_connect.show_friends_list_help) #Opens the friends list section of the how to play window when clicked
        self.help.store_button.clicked.connect(self.button_connect.show_store_help) #Opens the store section of the how to play window when clicked
        self.help.head_to_head_button.clicked.connect(self.button_connect.show_head_to_head_help) #Opens the head to head section of the how to play window when clicked


    def line_edits(self): #Connects each text user input
        self.ui.text_picture_name_1.returnPressed.connect(lambda: self.club.in_active_squad(1))
        self.ui.text_picture_name_2.returnPressed.connect(lambda: self.club.in_active_squad(2))
        self.ui.text_picture_name_3.returnPressed.connect(lambda: self.club.in_active_squad(3))
        self.ui.text_picture_name_4.returnPressed.connect(lambda: self.club.in_active_squad(4))
        self.ui.text_picture_name_5.returnPressed.connect(lambda: self.club.in_active_squad(5))

        self.ui.add_user.returnPressed.connect(self.friends_list.add_friend)

    def error_boxes(self, error_text): #When called, displays an error box with a message that is passed into it as a parameter
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(error_text)
        msg.setIcon(QMessageBox.Critical)
        execute = msg.exec_()

    def information_box(self, text): #When called, displays an information box with a message that is passed into it as a parameter
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText(text)
        msg.setIcon(QMessageBox.Information)
        execute = msg.exec_()
    

    def show(self): #Loads the user data and displays the GUI when called
        self.main_win.show() #Displayes the GUI
        self._run_api_task(
            "initial_core",
            lambda: self.request("get_dashboard"),
        )
        self._run_api_task(
            "initial_aux",
            lambda: (
                self.request("friends_list"),
                self.request("get_unassigned")["cards"],
            ),
        )
        
        self.loop_timer = QTimer(self.main_win)
        self.loop_timer.timeout.connect(self.refresh_account_data)
        self.loop_timer.start(5000)
        #Loop timer that is called every 3 seconds. Provides updates to the GUI when an action needs to be displayed

    def close(self):
        self._closed = True
        if hasattr(self, "loop_timer"):
            self.loop_timer.stop()
        self.pack_window.close()
        self.help_window.close()
        self.main_win.close()

class button_connect: #Class that connects all the main widget and navigation buttons 
    def __init__(self, main_window): #Accesses all atributes in MainWindow class
        self.main_window = main_window
    def loggedout(self): #Takes the user back to the login page when the log out button is clicked
        try:
            self.main_window.request("logout")
        except (ApiError, OSError, ValueError) as error:
            self.main_window.error_boxes(
                f"Could not confirm logout with the server: {error}"
            )
        finally:
            self.main_window.nav.session_token = None
            self.main_window.nav.show_login()

    def showHomepage(self):  #Goes to the homepage when Main Page button is clicked
        self.main_window.ui.stacked_widget.setCurrentWidget(self.main_window.ui.homepage)

    def showClub(self): #Goes to the user's club when the club button is clicked
        self.main_window.ui.stacked_widget.setCurrentWidget(self.main_window.ui.club)
        self.main_window.club.load_user_cards()
        self.main_window.club.resume_card_loading()

    def showTransfer_market(self): #Goes to the transfer market when the transfer market button is clicked
        self.main_window.ui.stacked_widget.setCurrentWidget(self.main_window.ui.transfer_market)

    def showFriends_list(self): #Goes to the friends list when the friends list button is clicked
        self.main_window.ui.stacked_widget.setCurrentWidget(self.main_window.ui.friends_list)

    def showStore(self): #Goes to the store when the store button is clicked
        self.main_window.ui.stacked_widget.setCurrentWidget(self.main_window.ui.store)
    
    def playGame(self): #Opens the head-to-head game when head-to-head button is clicked
        try:
            if self.main_window.club.pic1 and self.main_window.club.pic2 and self.main_window.club.pic3 and self.main_window.club.pic4 and self.main_window.club.pic5 is not None:
                self.main_window.nav.show_game()
            else:
                self.main_window.error_boxes("You do not have enough players in your active squad")
            #The user's active squad is checked to make sure users without all 5 players in their active squad can't start a game
        except Exception as e:
            print(e)

    def show_help(self): #Opens the how to play window when the how to play button is clicked
        self.main_window.help_window.show()

    def show_club_help(self): #Opens the club section of the how to play window when the club button is clicked
        self.main_window.help.stackedWidget.setCurrentWidget(self.main_window.help.club)
    
    def show_friends_list_help(self): #Opens the friends list section of the how to play window when the friends list button is clicked
        self.main_window.help.stackedWidget.setCurrentWidget(self.main_window.help.friends_list)
    
    def show_store_help(self): #Opens the store section of the how to play window when the store button is clicked
        self.main_window.help.stackedWidget.setCurrentWidget(self.main_window.help.store)

    def show_head_to_head_help(self): #Opens the head to head section of the how to play window when the head to head button is clicked
        self.main_window.help.stackedWidget.setCurrentWidget(self.main_window.help.head_to_head)

class club: #Club class of the game 
    def __init__(self, main_window): #Accesses all atributes in MainWindow class
        self.main_window = main_window
        self._card_paths = []
        self._card_index = 0
        self._card_load_generation = 0
        self._scheduled_card_batch_generation = None

    def update_account(self):
        profile = self.main_window.request("get_profile")
        self.apply_account(profile)

    def apply_account(self, profile):
        self.main_window.ui.record.setText(profile["record_text"])
        self.main_window.ui.coin_balance.setText(profile["balance_text"])


    def load_user_cards(self, force=False): #Function to load and display the cards in the user's club
        if self.main_window._club_cards_loaded and not force:
            return
        if force:
            self.main_window._club_cards_loaded = False
        self.main_window._run_api_task(
            "club", lambda: self.main_window.request("get_club")["cards"]
        )

    def display_user_cards(self, cards):
        for child in self.main_window.ui.scrollAreaWidgetContents_club.findChildren(QtWidgets.QLabel):
            child.deleteLater()
        self._card_load_generation += 1
        self._card_paths = cards
        self._card_index = 0
        self.main_window._club_cards_loaded = True
        self.resume_card_loading()

    def resume_card_loading(self):
        if (
            not self.main_window._club_cards_loaded
            or self._card_index >= len(self._card_paths)
            or self.main_window.ui.stacked_widget.currentWidget()
            is not self.main_window.ui.club
            or self._scheduled_card_batch_generation
            == self._card_load_generation
        ):
            return
        generation = self._card_load_generation
        self._scheduled_card_batch_generation = generation
        QTimer.singleShot(8, lambda: self._add_club_cards_batch(generation))

    def _add_club_cards_batch(self, generation):
        if self._scheduled_card_batch_generation == generation:
            self._scheduled_card_batch_generation = None
        if (
            generation != self._card_load_generation
            or not self.main_window._club_cards_loaded
            or self.main_window.ui.stacked_widget.currentWidget()
            is not self.main_window.ui.club
        ):
            return
        end = min(self._card_index + 4, len(self._card_paths))
        while self._card_index < end:
            self.update_club(self._card_paths[self._card_index], self._card_index)
            self._card_index += 1
        if self._card_index < len(self._card_paths):
            self.resume_card_loading()

    
    def load_user_active_squad(self): #Function which displays the user's active squad
        slots = self.main_window.request("get_squad")["slots"]
        self.apply_active_squad(slots)

    def apply_active_squad(self, slots):
        for index, slot in enumerate(slots, start=1):
            getattr(self.main_window.ui, f"text_picture_name_{index}").setText(
                slot["name"] or ""
            )
            frame = getattr(self.main_window.ui, f"picture_frame_{index}")
            frame.setPixmap(card_pixmap(slot["image"] or ""))
            setattr(self, f"pic{index}", frame.pixmap() if slot["image"] else None)
    
    
    def update_club(self, str_indiv_player, i): #Function which adds card labels to the user's club
        card_label = QtWidgets.QLabel(f"club_card{i}") #Creates a new label for the card
        self.configureLabel(card_label, str_indiv_player) #Calls the function to set the image of the label
        row, col = divmod(i, 5) #To ensure 5 cards are added per row
        self.main_window.ui.scrollAreaWidgetContents_club_layout.addWidget(card_label, row, col) #Adds the label to the layout of the user's club
     
    
    def configureLabel(self, card_label, str_indiv_player): #Function to configure each label added into the user's club
        card_label.setPixmap(card_pixmap (str_indiv_player)) #Sets the image of the label as the image path of the card
        card_label.setScaledContents(True) #Ensures the image is loaded correctly
        card_label.setStyleSheet("border: 0px solid black;") #Removes the border of the label
        card_label.setFixedSize(141, 181) #Sets a fixed size for each card label
    
    
    def in_active_squad(self, line_id): #Function which stores the text of each input field of the active squad
        if line_id == 1:
            user_input = self.main_window.ui.text_picture_name_1.text() #Gets the text inputted by the user (text input 1)
            text_id = 1
        
        if line_id == 2:
            user_input = self.main_window.ui.text_picture_name_2.text() #Gets the text inputted by the user (text input 2)
            text_id = 2
        
        if line_id == 3:
            user_input = self.main_window.ui.text_picture_name_3.text() #Gets the text inputted by the user (text input 3)
            text_id = 3
        
        if line_id == 4:
            user_input = self.main_window.ui.text_picture_name_4.text() #Gets the text inputted by the user (text input 4)
            text_id = 4
        
        if line_id == 5:
            user_input = self.main_window.ui.text_picture_name_5.text() #Gets the text inputted by the user (text input 5)
            text_id = 5
        
        self.name_check(user_input, text_id) #Calls the function to validate the user input

        
    def name_check(self, user_input, text_id): #Function which validates the user input in the active squad
        text_1 = self.main_window.ui.text_picture_name_1.text()
        text_2 = self.main_window.ui.text_picture_name_2.text()
        text_3 = self.main_window.ui.text_picture_name_3.text()
        text_4 = self.main_window.ui.text_picture_name_4.text()
        text_5 = self.main_window.ui.text_picture_name_5.text()
        #Stores the current text of each of the active squad input fields

        if user_input == "":
            self.main_window.error_boxes("No Name Entered") #Checks if there was a name entered and returns an appropriate error message
        else:
            try:
                updated = self.main_window.request(
                    "set_squad_slot", slot=text_id, name=user_input
                )
                slots = updated["slots"]
                for index, slot in enumerate(slots, start=1):
                    getattr(self.main_window.ui, f"text_picture_name_{index}").setText(
                        slot["name"] or ""
                    )
                    frame = getattr(self.main_window.ui, f"picture_frame_{index}")
                    frame.setPixmap(card_pixmap(slot["image"] or ""))
                    setattr(self, f"pic{index}", frame.pixmap() if slot["image"] else None)

            except Exception as e:
                self.main_window.error_boxes(str(e))


class friends_list(): #Class which handles the friends list logic
    def __init__(self, main_window):
        self.main_window = main_window #Accesses all atributes in MainWindow class
        self._displayed_friends = None
        self._displayed_friend_requests = None
        self._displayed_challenge_requests = None
        
        self.name_x = 10
        self.name_y = 10
        self.name_width = 121
        self.name_height = 21
        #Geometrics of the name labels

        self.inc_name_x = 10
        self.inc_name_y = 12
        #Geometrics of the incoming friend request name labels

        self.inc_challenge_name_x = 254
        self.inc_challenge_name_y = 12
        #Geometrics of the incoming challenge request name labels

        self.button_width = 61
        self.button_height = 31
        #Size of each button

        self.challenge_x = 137
        self.challenge_y = 7
        #Geometrics of the challenge friend buttons

        self.remove_x = 200
        self.remove_y = 7
        #Geometrics of the remove friend buttons

        self.friend_accept_x = 123
        self.friend_accept_y = 6
        #Geometrics of the accept friend request buttons

        self.friend_decline_x = 186
        self.friend_decline_y = 6
        #Geometrics of the decline friend request buttons

        self.challenge_accept_x = 375
        self.challenge_accept_y = 6
        #Geometrics of the accept challenge request buttons

        self.challenge_decline_x = 437
        self.challenge_decline_y = 6
        #Geometrics of the decline challenge request buttons
        

    def load_friends(self, data=None): #Function which displays the user's friends list
        if data is None:
            data = self.main_window.request("friends_list")
        all_friends_names = data["friends"]
        if all_friends_names == self._displayed_friends:
            return
        self._displayed_friends = list(all_friends_names)

        for child in self.main_window.ui.friends_list_frame.findChildren(QtWidgets.QLabel): #Deletes all labels stored in the friends list frame. Allows for constant refreshing of the friends list
            child.deleteLater()
        
        for child in self.main_window.ui.friends_list_frame.findChildren(QtWidgets.QPushButton): #Deletes all buttons stored in the friends list frame. Allows for constant refreshing of the friends list
            child.deleteLater()

        for i, str_indiv_friends_name in enumerate(all_friends_names):
            self.load_friends_list(str_indiv_friends_name, i)
            #The user name is accessed from the list sent by the server and iterated through. The names are converted to string for and added into the function to be displayed on the GUI

    
    def load_friends_list(self, indiv_friends_name, i): #Function which creates the labels and buttons necessary for the friends list
        friend_label = QtWidgets.QLabel(self.main_window.ui.friends_list_frame)
        friend_label.setObjectName(f"friend_label{i}")
        #Creates the label which stores the name of the other friend and adds it to the friends list frame

        challenge_button = QtWidgets.QPushButton(self.main_window.ui.friends_list_frame)
        challenge_button.setObjectName(f"challenge_button{i}")
        #Creates the button which challenges another friend to a game and adds it to the friends list frame

        remove_friend_button = QtWidgets.QPushButton(self.main_window.ui.friends_list_frame)
        remove_friend_button.setObjectName(f"remove_friend_button{i}")
        #Creates the button which removes another friend and adds it to the friends list frame
        
        self.configure_friend_list_label(friend_label, indiv_friends_name, i)
        self.configureChallenge(challenge_button, i)
        self.configureRemove(remove_friend_button, i)
        #Calls each function responsible for setting the geometry of each label and button

    
    def add_friend(self): #Function which handles the logic of sending a friend request to another user
        try:
            user_input = self.main_window.ui.add_user.text() #Gets the user input

            if user_input == "":
                self.main_window.error_boxes("No Name Was Entered")
            #Checks to see if a name was entered by the user. If not, an error is returned
            
            else:
                result = self.main_window.request(
                    "add_friend", username=user_input
                )["status"]
                self.main_window.information_box(result)
                #Displays the result from the server
        except Exception as e:
            self.main_window.error_boxes(str(e))

    def approved_friend_request(self, request_name): #Function which handles the logic of accepting a friend request
        self.main_window.request(
            "respond_request", username=request_name, accept=True
        )
        self.main_window.information_box("Successfully added user")


    def rejected_friend_request(self, request_name):
        self.main_window.request(
            "respond_request", username=request_name, accept=False
        )
        self.main_window.information_box("Successfully rejected friend request")
    
    def delete_from_friends(self, name):
        self.main_window.request("remove_friend", username=name)
        self.main_window.information_box("Successfully removed friend")

    def initiate_challenge(self, name): #Function which handles the logic of when a user challenges a friend to a game
        try:
            if self.main_window.club.pic1 and self.main_window.club.pic2 and self.main_window.club.pic3 and self.main_window.club.pic4 and self.main_window.club.pic5 is not None:
                #Checks if the user has a full active squad
                
                self.main_window.request("challenge_friend", username=name)

                msg = QMessageBox()
                msg.setWindowTitle("Challenge sent")
                msg.setText(f"Challenge sent to {name}. Waiting for them to accept.")
                msg.setIcon(QMessageBox.Information)
                msg.addButton(QMessageBox.Ok)
                msg.exec_()
                self.open_game("challenge")
                #Creates and executes the message box when the function is called

            else:
                self.main_window.error_boxes("You do not have enough players in your active squad")
                #Returns an error message if there are not enough players in the user's active squad

        except Exception as e:
            print(e)

    def open_game(self, mode="random"):
        self.main_window.nav.show_game(mode)
    
    def approved_challenge_request(self, request_name): #Function which handles the logic of when the user accepts a challenge request
        try:
            if self.main_window.club.pic1 and self.main_window.club.pic2 and self.main_window.club.pic3 and self.main_window.club.pic4 and self.main_window.club.pic5 is not None:
                #Checks if the user has a full active squad
                
                self.main_window.request(
                    "respond_challenge", username=request_name, accept=True
                )

                msg = QMessageBox()
                msg.setWindowTitle("Challenge accepted")
                msg.setText(f"You are now joining {request_name}.")
                msg.setIcon(QMessageBox.Information)
                msg.addButton(QMessageBox.Ok)
                msg.exec_()
                self.open_game("challenge")
                #Creates and executes the message box when the function is called

            else:
                self.main_window.error_boxes("You do not have enough players in your active squad")

        except Exception as e:
            print(e)


    def rejected_challenge_request(self, request_name): #Function which handles the logic of when the user rejects a challenge request
        self.main_window.request(
            "respond_challenge", username=request_name, accept=False
        )
        self.main_window.information_box("Successfully rejected challenge request")
    
    def show_incoming_friend_requests(self, data=None): #Function which displays any incoming friend requests
        try:
            if data is None:
                data = self.main_window.request("friends_list")
            names = data["friend_requests"]
            if names == self._displayed_friend_requests:
                return
            self._displayed_friend_requests = list(names)
            for child in self.main_window.ui.incoming_frame.findChildren(QtWidgets.QLabel):
                if child.objectName().startswith("incoming_friend_request_label"):
                    child.deleteLater()
            for child in self.main_window.ui.incoming_frame.findChildren(QtWidgets.QPushButton):
                if child.objectName().startswith(("accept_button", "decline_button")):
                    child.deleteLater()
            for index, name in enumerate(names):
                label = QtWidgets.QLabel(self.main_window.ui.incoming_frame)
                label.setObjectName(f"incoming_friend_request_label{index}")
                accept = QtWidgets.QPushButton(self.main_window.ui.incoming_frame)
                accept.setObjectName(f"accept_button{index}")
                decline = QtWidgets.QPushButton(self.main_window.ui.incoming_frame)
                decline.setObjectName(f"decline_button{index}")
                self.configure_incoming_friend_label(label, name, index)
                self.configure_friend_accept(accept, index)
                self.configure_friend_decline(decline, index)
        except Exception as e:
            print(e)

    def show_incoming_challenge_requests(self, data=None): #Function which displays the incoming challenge requests
        try:
            if data is None:
                data = self.main_window.request("friends_list")
            names = data["challenge_requests"]
            if names == self._displayed_challenge_requests:
                return
            self._displayed_challenge_requests = list(names)
            for child in self.main_window.ui.incoming_frame.findChildren(QtWidgets.QLabel):
                if child.objectName().startswith("incoming_challenge_request_label"):
                    child.deleteLater()
            for child in self.main_window.ui.incoming_frame.findChildren(QtWidgets.QPushButton):
                if child.objectName().startswith(("challenge_accept_button", "challenge_decline_button")):
                    child.deleteLater()
            for index, name in enumerate(names):
                label = QtWidgets.QLabel(self.main_window.ui.incoming_frame)
                label.setObjectName(f"incoming_challenge_request_label{index}")
                accept = QtWidgets.QPushButton(self.main_window.ui.incoming_frame)
                accept.setObjectName(f"challenge_accept_button{index}")
                decline = QtWidgets.QPushButton(self.main_window.ui.incoming_frame)
                decline.setObjectName(f"challenge_decline_button{index}")
                self.configure_incoming_challenge_label(label, name, index)
                self.configure_challenge_accept(accept, index)
                self.configure_challenge_decline(decline, index)
        except Exception as e:
            print(e)


    def configure_friend_list_label(self, friend_label, user_input, list_number): #Function which configures all name labels of added friends
        try:
            number = list_number * 44

            friend_label.setStyleSheet("""font: 16pt MS Shell Dlg 2; 
    border: 0px solid black;                                   
    """)
            friend_label.setGeometry(self.name_x, (self.name_y + number), self.name_width, self.name_height)
            friend_label.setText(user_input)
            friend_label.show()
            #Sets the geometry of each label along with setting the name and font of the other user label

        except Exception as e:
            print(e)
    
    def configureChallenge(self, challenge_button, list_number): #Function which configures the challenge button
        try:
            number = list_number * 43
            challenge_button.setGeometry(self.challenge_x, (self.challenge_y + number), self.button_width, self.button_height)
            challenge_button.setText("Challenge")
            challenge_button.clicked.connect(lambda: self.challenge_friend(challenge_button)) #When clicked, runs the challenge friend function and passes in the button clicked as a parameter
            challenge_button.show()
            #Sets the geometry of each button along with setting the name of the button
        except Exception as e:
            print(e)

    def configureRemove(self, remove_friend_button, list_number): #Function which configures the remove friend button
        try:
            number = list_number * 43
            remove_friend_button.setGeometry(self.remove_x, (self.remove_y + number), self.button_width, self.button_height)
            remove_friend_button.setText("Remove")
            remove_friend_button.clicked.connect(lambda: self.remove_friend(remove_friend_button)) #When clicked, runs the remove friend function and passes in the button clicked as a parameter
            remove_friend_button.show()
            #Sets the geometry of each button along with setting the name of the button
        except Exception as e:
            print(e)

    def configure_incoming_friend_label(self, label, name, i): #Function which configures all name labels of incoming friend requests
        try:
            number = i * 43
            
            label.setStyleSheet("""font: 16pt MS Shell Dlg 2; 
    border: 0px solid black;                                   
    """)
            label.setGeometry(self.inc_name_x, (self.inc_name_y + number), self.name_width, self.name_height)
            label.setText(name)
            label.show()
            #Sets the geometry of each label along with setting the name and font of the other user label

        except Exception as e:
            print(e)
    
    def configure_friend_accept(self, accept_button, i): #Function which configures the add friend button
        try:
            number = i * 43

            accept_button.setGeometry(self.friend_accept_x, (self.friend_accept_y + number), self.button_width, self.button_height)
            accept_button.setText("Accept")
            accept_button.clicked.connect(lambda: self.accept_friend_request(accept_button)) #When clicked, runs the accpet friend request function and passes in the button clicked as a parameter
            accept_button.show()
            #Sets the geometry of each button along with setting the name of the button
        
        except Exception as e:
            print(e)
    
    def configure_friend_decline(self, decline_button, i): #Function which configures the decline friend request button
        try:
            number = i * 43

            decline_button.setGeometry(self.friend_decline_x, (self.challenge_decline_y + number), self.button_width, self.button_height)
            decline_button.setText("Decline")
            decline_button.clicked.connect(lambda: self.decline_friend_request(decline_button)) #When clicked, runs the decline friend request function and passes in the button clicked as a parameter
            decline_button.show()
            #Sets the geometry of each button along with setting the name of the button

        except Exception as e:
            print(e)

    def accept_friend_request(self, clicked_button): #Function which gets the name of the other user corresponding to the accept friend request button pressed
        try:
            object_name = clicked_button.objectName() #Gets the object name of the button clicked
            subtract = "accept_button"

            object_number = object_name.replace(subtract, "") #Gets the object number of the button clicked
            
            label_name = f"incoming_friend_request_label{object_number}" #Assigns the name of the label corresponding to the button clicked as a variable
            prev_label = self.main_window.ui.incoming_frame.findChild(QtWidgets.QLabel, label_name) #Gets the object name of the label corresponding to the button clicked
            request_name = prev_label.text() #Gets the name of the other user corresponding to the button clicked
            
            self.approved_friend_request(request_name) #Passes the name as a parameter to the approve friend request function
        except Exception as e:
            print(e)

    def decline_friend_request(self, clicked_button): #Function which gets the name of the other user corresponding to the decline friend request button pressed
        try:
            object_name = clicked_button.objectName() #Gets the object name of the button clicked
            subtract = "decline_button"

            object_number = object_name.replace(subtract, "") #Gets the object number of the button clicked
            
            label_name = f"incoming_friend_request_label{object_number}" #Assigns the name of the label corresponding to the button clicked as a variable
            prev_label = self.main_window.ui.incoming_frame.findChild(QtWidgets.QLabel, label_name) #Gets the object name of the label corresponding to the button clicked
            request_name = prev_label.text() #Gets the name of the other user corresponding to the button clicked
            
            self.rejected_friend_request(request_name) #Passes the name as a parameter to the reject friend request function
        except Exception as e:
            print(e)

    def remove_friend(self, clicked_button): #Function which gets the name of the other user corresponding to the remove friend button pressed
        try:
            object_name = clicked_button.objectName() #Gets the object name of the button clicked
            subtract = "remove_friend_button"

            object_number = object_name.replace(subtract, "") #Gets the object number of the button clicked

            label_name = f"friend_label{object_number}" #Assigns the name of the label corresponding to the button clicked as a variable
            prev_label = self.main_window.ui.friends_list_frame.findChild(QtWidgets.QLabel, label_name) #Gets the object name of the label corresponding to the button clicked
            name = prev_label.text() #Gets the name of the other user corresponding to the button clicked

            self.delete_from_friends(name) #Passes the name as a parameter to the delete from friends list function
        except Exception as e:
            print(e)

    def challenge_friend(self, challenge_button): #Function which gets the name of the other user corresponding to the challenge friend button pressed
        try:
            object_name = challenge_button.objectName() #Gets the object name of the button clicked
            subtract = "challenge_button"

            object_number = object_name.replace(subtract, "") #Gets the object number of the button clicked

            label_name = f"friend_label{object_number}" #Assigns the name of the label corresponding to the button clicked as a variable
            prev_label = self.main_window.ui.friends_list_frame.findChild(QtWidgets.QLabel, label_name) #Gets the object name of the label corresponding to the button clicked
            name = prev_label.text() #Gets the name of the other user corresponding to the button clicked

            self.initiate_challenge(name) #Passes the name as a parameter to the challenge friend function
        except Exception as e:
            print(e)
    
    def configure_incoming_challenge_label(self, label, name, i): #Function which configures all name labels of incoming challenge requests
        try:
            number = i * 43
            
            label.setStyleSheet("""font: 16pt MS Shell Dlg 2; 
    border: 0px solid black;                                   
    """)
            label.setGeometry(self.inc_challenge_name_x, (self.inc_challenge_name_y + number), self.name_width, self.name_height)
            label.setText(name)
            label.show()
            #Sets the geometry of each label along with setting the name and font of the other user label

        except Exception as e:
            print(e)

    def configure_challenge_accept(self, accept_button, i): #Function which configures the accept challenge request button
        try:
            number = i * 43

            accept_button.setGeometry(self.challenge_accept_x, (self.challenge_accept_y + number), self.button_width, self.button_height)
            accept_button.setText("Accept")
            accept_button.clicked.connect(lambda: self.accept_challenge_request(accept_button)) #When clicked, runs the accpet challenge request function and passes in the button clicked as a parameter
            accept_button.show()
            #Sets the geometry of each button along with setting the name of the button
        except Exception as e:
            print(e)
    
    def configure_challenge_decline(self, decline_button, i): #Function which configures the decline challenge request button
        try:
            number = i * 43

            decline_button.setGeometry(self.challenge_decline_x, (self.challenge_decline_y + number), self.button_width, self.button_height)
            decline_button.setText("Decline")
            decline_button.clicked.connect(lambda: self.decline_challenge_request(decline_button)) #When clicked, runs the decline challenge request function and passes in the button clicked as a parameter
            decline_button.show()
            #Sets the geometry of each button along with setting the name of the button

        except Exception as e:
            print(e)

    def accept_challenge_request(self, clicked_button): #Function which gets the name of the other user corresponding to the accept challenge request button pressed
        try:
            object_name = clicked_button.objectName() #Gets the object name of the button clicked
            subtract = "challenge_accept_button"

            object_number = object_name.replace(subtract, "") #Gets the object number of the button clicked
            
            label_name = f"incoming_challenge_request_label{object_number}" #Assigns the name of the label corresponding to the button clicked as a variable
            prev_label = self.main_window.ui.incoming_frame.findChild(QtWidgets.QLabel, label_name) #Gets the object name of the label corresponding to the button clicked
            request_name = prev_label.text() #Gets the name of the other user corresponding to the button clicked
            
            self.approved_challenge_request(request_name) #Passes the name as a parameter to the approve challenge request function
        except Exception as e:
            print(e)

    def decline_challenge_request(self, clicked_button): #Function which gets the name of the other user corresponding to the decline challenge request button pressed
        try:
            object_name = clicked_button.objectName() #Gets the object name of the button clicked
            subtract = "challenge_decline_button"

            object_number = object_name.replace(subtract, "") #Gets the object number of the button clicked
            
            label_name = f"incoming_challenge_request_label{object_number}" #Assigns the name of the label corresponding to the button clicked as a variable
            prev_label = self.main_window.ui.incoming_frame.findChild(QtWidgets.QLabel, label_name) #Gets the object name of the label corresponding to the button clicked
            request_name = prev_label.text() #Gets the name of the other user corresponding to the button clicked
            
            self.rejected_challenge_request(request_name) #Passes the name as a parameter to the reject challenge request function
        except Exception as e:
            print(e)


class store: #Class which handles all functions related with the store
    def __init__(self, main_window):
        self.main_window = main_window #Accesses all atributes in MainWindow class
        self.label_list = [] #Creates an empty list used later to store labels of cards
        self.buy_pack() #Calls the function which stores the button presses for each pack

    def check_unassigned(self, name_path_list=None): #Function which checks if the user has any unassigned items to deal with
        if name_path_list is None:
            name_path_list = self.main_window.request("get_unassigned")["cards"]
        if name_path_list:
            self.main_window.error_boxes("You have unassigned items to deal with") #Displays the error message to the GUI
            self.label_list = []
            for i, image_path in enumerate(name_path_list):
                self.load_unassigned_cards(image_path, i)
                #Starts the function to display the unassigned items with each image path being passed in as a parameter along with the number corresponding to it

            self.main_window.pack_window.show() #Shows the window containing the user's unassigned cards
            self.main_window.main_win.hide() #Closes the Main Menu window
    
    def buy_pack(self): #Function which connects the "buy pack" button presses
        try:
            self.main_window.ui.purchase_pack1.clicked.connect(lambda: self.get_items(10, 10000))
            self.main_window.ui.purchase_pack2.clicked.connect(lambda: self.get_items(30, 25000))
            self.main_window.ui.purchase_pack3.clicked.connect(lambda: self.get_items(50, 45000))
            #Depending on the pack purchased, the number of cards and cost of the pack are passed into the parameter
        
        except Exception as e:
            print(e)


    def get_items(self, number, pack_cost): #Function which gets the cards to be displayed after opening a pack
        try:
            result = self.main_window.request("buy_pack", pack=pack_cost)
            self.label_list = []
            for index, image_path in enumerate(result["cards"]):
                self.load_pack(image_path, index)
            self.main_window.pack_window.show()
            self.main_window.main_win.hide()
        except Exception as e:
            self.main_window.error_boxes(str(e))

    
    def load_unassigned_cards(self, player_path, i): #Function which adds card labels to the unassigned cards display
        try:
            card_label = QtWidgets.QLabel()
            card_label.setObjectName(f"packed_card{i}") #Creates a new label for the card
            self.configure_label(card_label, player_path) #Calls the function to set the image of the label
            row, col = divmod(i, 5) #To ensure 5 cards are added per row

            store_items_button = QtWidgets.QPushButton(self.main_window.pack.centralwidget)
            store_items_button.setObjectName("store_items_button") #Creates a button used for storing all cards in the pack
            self.configure_store_button(store_items_button) #Sends the button to be configured

            self.main_window.pack.scrollAreaWidgetContents_show_packed_cards_layout.addWidget(card_label, row, col) #Adds the label to the pack layout
        except Exception as e:
            print(e)

    
    def load_pack(self, player_path, i): #Function which adds card labels to the pack display
        try:
            card_label = QtWidgets.QLabel()
            card_label.setObjectName(f"packed_card{i}") #Creates a new label for the card
            self.configure_label(card_label, player_path) #Calls the function to set the image of the label
            row, col = divmod(i, 5) #To ensure 5 cards are added per row

            store_items_button = QtWidgets.QPushButton(self.main_window.pack.centralwidget)
            store_items_button.setObjectName("store_items_button") #Creates a button used for storing all cards in the pack
            self.configure_store_button(store_items_button) #Sends the button to be configured

            self.main_window.pack.scrollAreaWidgetContents_show_packed_cards_layout.addWidget(card_label, row, col) #Adds the label to the pack layout
        except Exception as e:
            print(e)

    
    def configure_label(self, card_label, player_path): #Function to configure each label added into each pack
        card_label.setPixmap(card_pixmap (player_path)) #Sets the image of the label as the image path of the card
        card_label.setScaledContents(True) #Ensures the image is loaded correctly
        card_label.setStyleSheet("border: 0px solid black;") #Removes the border of the label
        card_label.setFixedSize(141, 181) #Sets a fixed size for each card label
        self.label_list.append(player_path) #Stores each card in the list of all cards in a pack

    def store_items(self): #Function which handles the logic of storing players in a pack
        try:
            result = self.main_window.request("store_pack", cards=self.label_list)
            list_of_dupe_items = result["duplicates"]
            if list_of_dupe_items:
                self.label_list = []
                self.main_window.error_boxes("You have duplicate items to deal with")

                for child in self.main_window.pack.scrollAreaWidgetContents_show_packed_cards.findChildren(QtWidgets.QWidget): #Deletes all cards stored in the pack
                    child.deleteLater()

                for child in self.main_window.pack.centralwidget.findChildren(QtWidgets.QPushButton): #Deletes the store items button
                    child.deleteLater()

                for i, image_path in enumerate(list_of_dupe_items):
                    self.load_pack(image_path, i)
                    #Starts the function to display the cards in the pack with each image path being passed in as a parameter along with the number corresponding to it 
                    
                    quick_sell = QtWidgets.QPushButton(self.main_window.pack.centralwidget)
                    quick_sell.setObjectName("quick_sell") #Creates a button to quick sell all players in the pack

                    self.configure_sell_button(quick_sell, len(list_of_dupe_items))
                    #Starts the function and passes the button to quick sell all players and the number of duplicate players

            else:
                self.main_window.information_box("Successfully stored players") #Displays the message if no duplicate items are being stored in the user's club
                self.main_window.club.load_user_cards(force=True) #Function to display the added cards to the user's club
                self.main_window.pack_window.hide() #Hides the window containing the pack
                self.main_window.main_win.show() #Opens the Main Menu window

        except Exception as e:
            self.main_window.error_boxes(str(e))

    def configure_store_button(self, button): #Function which configures the store items button
        button.setGeometry(330, 20, 201, 61)
        button.setText("Store Items In Club")
        button.clicked.connect(self.store_items)
        button.show()
        #Sets the geometry and text of the store items button. Also connects the button with the store items function when clicked

    
    def configure_sell_button(self, quick_sell, num): #Function which configures the quick sell items button
        quick_sell.setGeometry(330, 20, 201, 61)
        quick_sell.setText("Quick sell all players")
        quick_sell.clicked.connect(lambda: self.quick_sold_players(num))
        quick_sell.show()
        #Sets the geometry and text of the quick sell items button. Also connects the button with the quick sell items function when clicked

    def quick_sold_players(self, num): #Function which handles the logic of when the quick sell all players button is clicked
        balance_update = self.main_window.request("quick_sell")["coins_added"]
        text = f"Successfully added {balance_update} coins to your account" #Text to be displayed on the GUI
        
        self.main_window.information_box(text) #Displays the messagebox to the GUI

        for child in self.main_window.pack.centralwidget.findChildren(QtWidgets.QPushButton): #Deletes the quick sell items button
            child.deleteLater()
        
        self.main_window.club.load_user_cards(force=True) #Function to display the added cards to the user's club
        self.main_window.pack_window.hide() #Hides the window containing the pack
        self.main_window.main_win.show() #Opens the Main Menu window
