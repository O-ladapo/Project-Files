from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(667, 643)
        MainWindow.setStyleSheet(
            "QMainWindow, QWidget { color: white; background-color: rgb(22, 22, 22); }"
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(22, 22, 22);")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.login_page = QtWidgets.QWidget()
        self.login_page.setObjectName("login_page")
        self.frame = QtWidgets.QFrame(self.login_page)
        self.frame.setGeometry(QtCore.QRect(0, 0, 641, 641))
        self.frame.setStyleSheet("background-color: rgb(22, 22, 22);")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setObjectName("frame")
        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setGeometry(QtCore.QRect(60, 30, 521, 571))
        self.widget.setStyleSheet("background-color: rgb(36, 36, 36);")
        self.widget.setObjectName("widget")
        self.login_label = QtWidgets.QLabel(self.widget)
        self.login_label.setGeometry(QtCore.QRect(220, 0, 91, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.login_label.setFont(font)
        self.login_label.setObjectName("login_label")
        self.username_textbox = QtWidgets.QLineEdit(self.widget)
        self.username_textbox.setGeometry(QtCore.QRect(160, 90, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.username_textbox.setFont(font)
        self.username_textbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.username_textbox.setStyleSheet("color: white;\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius: 15px;")
        self.username_textbox.setText("")
        self.username_textbox.setFrame(True)
        self.username_textbox.setObjectName("username_textbox")
        self.password_textbox = QtWidgets.QLineEdit(self.widget)
        self.password_textbox.setGeometry(QtCore.QRect(160, 170, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.password_textbox.setFont(font)
        self.password_textbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.password_textbox.setStyleSheet("color: white;\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius: 15px;")
        self.password_textbox.setText("")
        self.password_textbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_textbox.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.password_textbox.setObjectName("password_textbox")
        self.login_button = QtWidgets.QPushButton(self.widget)
        self.login_button.setGeometry(QtCore.QRect(160, 250, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.login_button.setFont(font)
        self.login_button.setStyleSheet(
            "QPushButton { border-radius: 15px; color: white; "
            "background-color: rgb(41, 121, 255); }\n"
            "QPushButton:hover { background-color: rgb(66, 165, 245); }"
        )
        self.login_button.setObjectName("login_button")
        self.signup_button = QtWidgets.QPushButton(self.widget)
        self.signup_button.setGeometry(QtCore.QRect(160, 330, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.signup_button.setFont(font)
        self.signup_button.setStyleSheet(
            "QPushButton { border-radius: 15px; color: white; "
            "background-color: rgb(41, 121, 255); }\n"
            "QPushButton:hover { background-color: rgb(66, 165, 245); }"
        )
        self.signup_button.setObjectName("signup_button")
        self.show_password_button = QtWidgets.QPushButton(self.widget)
        self.show_password_button.setGeometry(QtCore.QRect(180, 400, 31, 31))
        self.show_password_button.setStyleSheet(
            "QPushButton { border: 2px solid white; border-radius: 7px; "
            "background-color: transparent; color: transparent; "
            "font-size: 24px; font-weight: bold; padding: 0; }\n"
            "QPushButton:checked { color: white; "
            "background-color: rgb(41, 121, 255); }\n"
            "QPushButton:hover { background-color: rgb(66, 165, 245); }\n"
            "QPushButton:checked:hover { color: white; }"
        )
        self.show_password_button.setText("✓")
        self.show_password_button.setCheckable(True)
        self.show_password_button.setObjectName("show_password_button")
        self.show_password_label = QtWidgets.QLabel(self.widget)
        self.show_password_label.setGeometry(QtCore.QRect(220, 395, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.show_password_label.setFont(font)
        self.show_password_label.setObjectName("show_password_label")
        self.stackedWidget.addWidget(self.login_page)
        self.register_page = QtWidgets.QWidget()
        self.register_page.setObjectName("register_page")
        self.frame_2 = QtWidgets.QFrame(self.register_page)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 641, 641))
        self.frame_2.setStyleSheet("background-color: rgb(22, 22, 22);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setObjectName("frame_2")
        self.widget_2 = QtWidgets.QWidget(self.frame_2)
        self.widget_2.setGeometry(QtCore.QRect(60, 30, 521, 571))
        self.widget_2.setStyleSheet("background-color: rgb(36, 36, 36);")
        self.widget_2.setObjectName("widget_2")
        self.signup_label = QtWidgets.QLabel(self.widget_2)
        self.signup_label.setGeometry(QtCore.QRect(190, 0, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.signup_label.setFont(font)
        self.signup_label.setObjectName("signup_label")
        self.username_textbox_signup = QtWidgets.QLineEdit(self.widget_2)
        self.username_textbox_signup.setGeometry(QtCore.QRect(160, 90, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.username_textbox_signup.setFont(font)
        self.username_textbox_signup.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.username_textbox_signup.setStyleSheet("color: white;\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius: 15px;")
        self.username_textbox_signup.setText("")
        self.username_textbox_signup.setFrame(True)
        self.username_textbox_signup.setObjectName("username_textbox_signup")
        self.password_textbox_signup = QtWidgets.QLineEdit(self.widget_2)
        self.password_textbox_signup.setGeometry(QtCore.QRect(160, 170, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.password_textbox_signup.setFont(font)
        self.password_textbox_signup.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.password_textbox_signup.setStyleSheet("color: white;\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius: 15px;")
        self.password_textbox_signup.setText("")
        self.password_textbox_signup.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_textbox_signup.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.password_textbox_signup.setObjectName("password_textbox_signup")
        self.register_button = QtWidgets.QPushButton(self.widget_2)
        self.register_button.setGeometry(QtCore.QRect(160, 325, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.register_button.setFont(font)
        self.register_button.setStyleSheet(
            "QPushButton { border-radius: 15px; color: white; "
            "background-color: rgb(41, 121, 255); }\n"
            "QPushButton:hover { background-color: rgb(66, 165, 245); }"
        )
        self.register_button.setObjectName("register_button")
        self.already_registered_button = QtWidgets.QPushButton(self.widget_2)
        self.already_registered_button.setGeometry(QtCore.QRect(160, 405, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.already_registered_button.setFont(font)
        self.already_registered_button.setStyleSheet(
            "QPushButton { border-radius: 15px; color: white; "
            "background-color: rgb(41, 121, 255); }\n"
            "QPushButton:hover { background-color: rgb(66, 165, 245); }"
        )
        self.already_registered_button.setObjectName("already_registered_button")
        self.show_password_button_signup = QtWidgets.QPushButton(self.widget_2)
        self.show_password_button_signup.setGeometry(QtCore.QRect(180, 475, 31, 31))
        self.show_password_button_signup.setStyleSheet(
            "QPushButton { border: 2px solid white; border-radius: 7px; "
            "background-color: transparent; color: transparent; "
            "font-size: 24px; font-weight: bold; padding: 0; }\n"
            "QPushButton:checked { color: white; "
            "background-color: rgb(41, 121, 255); }\n"
            "QPushButton:hover { background-color: rgb(66, 165, 245); }\n"
            "QPushButton:checked:hover { color: white; }"
        )
        self.show_password_button_signup.setText("✓")
        self.show_password_button_signup.setCheckable(True)
        self.show_password_button_signup.setObjectName("show_password_button_signup")
        self.show_passwords_label = QtWidgets.QLabel(self.widget_2)
        self.show_passwords_label.setGeometry(QtCore.QRect(220, 470, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.show_passwords_label.setFont(font)
        self.show_passwords_label.setObjectName("show_passwords_label")
        self.confirm_password_textbox = QtWidgets.QLineEdit(self.widget_2)
        self.confirm_password_textbox.setGeometry(QtCore.QRect(160, 250, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.confirm_password_textbox.setFont(font)
        self.confirm_password_textbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.confirm_password_textbox.setStyleSheet("color: white;\n"
"background-color: rgb(50, 50, 50);\n"
"border-radius: 15px;")
        self.confirm_password_textbox.setText("")
        self.confirm_password_textbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_textbox.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.confirm_password_textbox.setObjectName("confirm_password_textbox")
        self.stackedWidget.addWidget(self.register_page)
        self.horizontalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.login_label.setText(_translate("MainWindow", "Login"))
        self.username_textbox.setPlaceholderText(_translate("MainWindow", "Username"))
        self.password_textbox.setPlaceholderText(_translate("MainWindow", "Password"))
        self.login_button.setText(_translate("MainWindow", "Login"))
        self.signup_button.setText(_translate("MainWindow", "Sign Up"))
        self.show_password_label.setText(_translate("MainWindow", "Show Password"))
        self.signup_label.setText(_translate("MainWindow", "Sign Up"))
        self.username_textbox_signup.setPlaceholderText(_translate("MainWindow", "Username"))
        self.password_textbox_signup.setPlaceholderText(_translate("MainWindow", "Password"))
        self.register_button.setText(_translate("MainWindow", "Register User"))
        self.already_registered_button.setText(_translate("MainWindow", "Already Registered?"))
        self.show_passwords_label.setText(_translate("MainWindow", "Show Passwords"))
        self.confirm_password_textbox.setPlaceholderText(_translate("MainWindow", "Confirm Password"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
