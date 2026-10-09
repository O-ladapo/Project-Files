from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HelpWindow(object):
    def setupUi(self, HelpWindow):
        HelpWindow.setObjectName("HelpWindow")
        HelpWindow.resize(661, 369)
        HelpWindow.setStyleSheet("background-color: rgb(191, 191, 191);")
        self.centralwidget = QtWidgets.QWidget(HelpWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.club_button = QtWidgets.QPushButton(self.centralwidget)
        self.club_button.setGeometry(QtCore.QRect(20, 20, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.club_button.setFont(font)
        self.club_button.setObjectName("club_button")
        self.friends_list_button = QtWidgets.QPushButton(self.centralwidget)
        self.friends_list_button.setGeometry(QtCore.QRect(180, 20, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.friends_list_button.setFont(font)
        self.friends_list_button.setObjectName("friends_list_button")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 90, 631, 281))
        self.stackedWidget.setObjectName("stackedWidget")
        self.club = QtWidgets.QWidget()
        self.club.setObjectName("club")
        self.club_text = QtWidgets.QTextBrowser(self.club)
        self.club_text.setGeometry(QtCore.QRect(10, 46, 601, 221))
        self.club_text.setStyleSheet("border: 1px solid black;")
        self.club_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.club_text.setObjectName("club_text")
        self.club_title = QtWidgets.QLabel(self.club)
        self.club_title.setGeometry(QtCore.QRect(290, 10, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.club_title.setFont(font)
        self.club_title.setObjectName("club_title")
        self.stackedWidget.addWidget(self.club)
        self.friends_list = QtWidgets.QWidget()
        self.friends_list.setObjectName("friends_list")
        self.friends_list_title = QtWidgets.QLabel(self.friends_list)
        self.friends_list_title.setGeometry(QtCore.QRect(260, 10, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.friends_list_title.setFont(font)
        self.friends_list_title.setObjectName("friends_list_title")
        self.friends_list_text1 = QtWidgets.QTextBrowser(self.friends_list)
        self.friends_list_text1.setGeometry(QtCore.QRect(10, 46, 601, 201))
        self.friends_list_text1.setStyleSheet("border: 1px solid black;")
        self.friends_list_text1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.friends_list_text1.setObjectName("friends_list_text1")
        self.stackedWidget.addWidget(self.friends_list)
        self.store = QtWidgets.QWidget()
        self.store.setObjectName("store")
        self.store_title = QtWidgets.QLabel(self.store)
        self.store_title.setGeometry(QtCore.QRect(290, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.store_title.setFont(font)
        self.store_title.setObjectName("store_title")
        self.store_text = QtWidgets.QTextBrowser(self.store)
        self.store_text.setGeometry(QtCore.QRect(10, 46, 601, 101))
        self.store_text.setStyleSheet("border: 1px solid black;")
        self.store_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.store_text.setObjectName("store_text")
        self.stackedWidget.addWidget(self.store)
        self.head_to_head = QtWidgets.QWidget()
        self.head_to_head.setObjectName("head_to_head")
        self.head_to_head_title = QtWidgets.QLabel(self.head_to_head)
        self.head_to_head_title.setGeometry(QtCore.QRect(250, 10, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.head_to_head_title.setFont(font)
        self.head_to_head_title.setObjectName("head_to_head_title")
        self.head_to_head_text = QtWidgets.QTextBrowser(self.head_to_head)
        self.head_to_head_text.setGeometry(QtCore.QRect(10, 46, 591, 191))
        self.head_to_head_text.setStyleSheet("border: 1px solid black;")
        self.head_to_head_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.head_to_head_text.setObjectName("head_to_head_text")
        self.stackedWidget.addWidget(self.head_to_head)
        self.store_button = QtWidgets.QPushButton(self.centralwidget)
        self.store_button.setGeometry(QtCore.QRect(340, 20, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.store_button.setFont(font)
        self.store_button.setObjectName("store_button")
        self.head_to_head_button = QtWidgets.QPushButton(self.centralwidget)
        self.head_to_head_button.setGeometry(QtCore.QRect(500, 20, 140, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.head_to_head_button.setFont(font)
        self.head_to_head_button.setObjectName("head_to_head_button")
        HelpWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(HelpWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(HelpWindow)

    def retranslateUi(self, HelpWindow):
        _translate = QtCore.QCoreApplication.translate
        HelpWindow.setWindowTitle(_translate("HelpWindow", "MainWindow"))
        self.club_button.setText(_translate("HelpWindow", "Club"))
        self.friends_list_button.setText(_translate("HelpWindow", "Friends List"))
        self.club_text.setHtml(_translate("HelpWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">You can input names of players you own in your active squad. To input names into the active squad, click the slot you want the player to be in. Then, type the players name into it. For harder to spell names, you can type some of thier name and it will be autofilled. For example, &quot;ka&quot; for &quot;Kane&quot;.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">These players will be used when you enter the head-to-head mode. Without a full active squad, you wont be allowed to enter the head-to-head mode. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p></body></html>"))
        self.club_title.setText(_translate("HelpWindow", "Club"))
        self.friends_list_title.setText(_translate("HelpWindow", "Friends List"))
        self.friends_list_text1.setHtml(_translate("HelpWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">You can add other users by simply typing in the users name and clicking enter. A friend request will be displayed on their screen, where they can choose to either accept or decline it.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">With an added friend, you can challenge them to a game. Simply click challenge and you will be presented with a game code which you can input. The challenge request will be displayed on the other user\'s screen where they can either accept or decline it.</span></p></body></html>"))
        self.store_title.setText(_translate("HelpWindow", "Store"))
        self.store_text.setHtml(_translate("HelpWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Coins can be obtained from winning games, which can be used to purchase packs in the store. Each pack will generate random players corresponding to the number of players in the pack. These players can be stored in the club or quick sold if a duplicate.</span></p></body></html>"))
        self.head_to_head_title.setText(_translate("HelpWindow", "Head-to-Head"))
        self.head_to_head_text.setHtml(_translate("HelpWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">You can select a card of your choice when the round is started. Cards selected will be disabled for future rounds. Opposing player cards can only be seen after both players have had thier turns to make the game fair. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">At the end of each round, the winner will be displayed along with the points tally. After 5 rounds, the winner of the game is displayed and all players are returned to the main menu.</span></p></body></html>"))
        self.store_button.setText(_translate("HelpWindow", "Store"))
        self.head_to_head_button.setText(_translate("HelpWindow", "Head-to-Head"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HelpWindow = QtWidgets.QMainWindow()
    ui = Ui_HelpWindow()
    ui.setupUi(HelpWindow)
    HelpWindow.show()
    sys.exit(app.exec_())
