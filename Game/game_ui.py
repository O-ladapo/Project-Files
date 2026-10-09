from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1138, 755)
        MainWindow.setStyleSheet("background-color: rgb(191, 191, 191);")
        self.main_homepage = QtWidgets.QWidget(MainWindow)
        self.main_homepage.setObjectName("main_homepage")
        self.nav_bar = QtWidgets.QFrame(self.main_homepage)
        self.nav_bar.setGeometry(QtCore.QRect(0, 0, 1131, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.nav_bar.setFont(font)
        self.nav_bar.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.nav_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nav_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nav_bar.setObjectName("nav_bar")
        self.main_page_button_nav = QtWidgets.QPushButton(self.nav_bar)
        self.main_page_button_nav.setGeometry(QtCore.QRect(0, 0, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.main_page_button_nav.setFont(font)
        self.main_page_button_nav.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.main_page_button_nav.setObjectName("main_page_button_nav")
        self.club_button_nav = QtWidgets.QPushButton(self.nav_bar)
        self.club_button_nav.setGeometry(QtCore.QRect(200, 0, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.club_button_nav.setFont(font)
        self.club_button_nav.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.club_button_nav.setObjectName("club_button_nav")
        self.transfer_market_button_nav = QtWidgets.QPushButton(self.nav_bar)
        self.transfer_market_button_nav.setGeometry(QtCore.QRect(400, 0, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.transfer_market_button_nav.setFont(font)
        self.transfer_market_button_nav.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.transfer_market_button_nav.setObjectName("transfer_market_button_nav")
        self.friends_list_button_nav = QtWidgets.QPushButton(self.nav_bar)
        self.friends_list_button_nav.setGeometry(QtCore.QRect(600, 0, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.friends_list_button_nav.setFont(font)
        self.friends_list_button_nav.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.friends_list_button_nav.setObjectName("friends_list_button_nav")
        self.store_button_nav = QtWidgets.QPushButton(self.nav_bar)
        self.store_button_nav.setGeometry(QtCore.QRect(800, 0, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.store_button_nav.setFont(font)
        self.store_button_nav.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.store_button_nav.setObjectName("store_button_nav")
        self.log_out_button_nav = QtWidgets.QPushButton(self.nav_bar)
        self.log_out_button_nav.setGeometry(QtCore.QRect(1000, 0, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.log_out_button_nav.setFont(font)
        self.log_out_button_nav.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.log_out_button_nav.setObjectName("log_out_button_nav")
        self.coin_balance = QtWidgets.QLabel(self.main_homepage)
        self.coin_balance.setGeometry(QtCore.QRect(900, 80, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.coin_balance.setFont(font)
        self.coin_balance.setStyleSheet("")
        self.coin_balance.setObjectName("coin_balance")
        self.record = QtWidgets.QLabel(self.main_homepage)
        self.record.setGeometry(QtCore.QRect(100, 80, 221, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.record.setFont(font)
        self.record.setStyleSheet("")
        self.record.setObjectName("record")
        self.stacked_widget = QtWidgets.QStackedWidget(self.main_homepage)
        self.stacked_widget.setGeometry(QtCore.QRect(10, 150, 1111, 581))
        self.stacked_widget.setObjectName("stacked_widget")
        self.homepage = QtWidgets.QWidget()
        self.homepage.setObjectName("homepage")
        self.head_to_head_button = QtWidgets.QPushButton(self.homepage)
        self.head_to_head_button.setGeometry(QtCore.QRect(140, 0, 421, 291))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.head_to_head_button.setFont(font)
        self.head_to_head_button.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.head_to_head_button.setObjectName("head_to_head_button")
        self.friends_list_button = QtWidgets.QPushButton(self.homepage)
        self.friends_list_button.setGeometry(QtCore.QRect(560, 0, 421, 291))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.friends_list_button.setFont(font)
        self.friends_list_button.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.friends_list_button.setObjectName("friends_list_button")
        self.store_button = QtWidgets.QPushButton(self.homepage)
        self.store_button.setGeometry(QtCore.QRect(560, 290, 421, 291))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.store_button.setFont(font)
        self.store_button.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.store_button.setObjectName("store_button")
        self.club_button = QtWidgets.QPushButton(self.homepage)
        self.club_button.setGeometry(QtCore.QRect(140, 290, 421, 291))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.club_button.setFont(font)
        self.club_button.setStyleSheet("QPushButton{\n"
"    background-color: rgb(41, 121, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(66, 165, 245);\n"
"}\n"
"")
        self.club_button.setObjectName("club_button")
        self.stacked_widget.addWidget(self.homepage)
        self.club = QtWidgets.QWidget()
        self.club.setObjectName("club")
        self.active_squad = QtWidgets.QFrame(self.club)
        self.active_squad.setGeometry(QtCore.QRect(10, 10, 291, 561))
        self.active_squad.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"}")
        self.active_squad.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.active_squad.setFrameShadow(QtWidgets.QFrame.Raised)
        self.active_squad.setObjectName("active_squad")
        self.active_squad_name = QtWidgets.QLabel(self.active_squad)
        self.active_squad_name.setGeometry(QtCore.QRect(80, 10, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.active_squad_name.setFont(font)
        self.active_squad_name.setStyleSheet("QFrame{\n"
"border: 0px solid black;\n"
"}")
        self.active_squad_name.setObjectName("active_squad_name")
        self.picture_frame_1 = QtWidgets.QLabel(self.active_squad)
        self.picture_frame_1.setGeometry(QtCore.QRect(10, 60, 71, 91))
        self.picture_frame_1.setStyleSheet("border: 1px solid black;")
        self.picture_frame_1.setText("")
        self.picture_frame_1.setScaledContents(True)
        self.picture_frame_1.setObjectName("picture_frame_1")
        self.picture_frame_2 = QtWidgets.QLabel(self.active_squad)
        self.picture_frame_2.setGeometry(QtCore.QRect(10, 160, 71, 91))
        self.picture_frame_2.setStyleSheet("border: 1px solid black;")
        self.picture_frame_2.setText("")
        self.picture_frame_2.setScaledContents(True)
        self.picture_frame_2.setObjectName("picture_frame_2")
        self.picture_frame_3 = QtWidgets.QLabel(self.active_squad)
        self.picture_frame_3.setGeometry(QtCore.QRect(10, 260, 71, 91))
        self.picture_frame_3.setStyleSheet("border: 1px solid black;")
        self.picture_frame_3.setText("")
        self.picture_frame_3.setScaledContents(True)
        self.picture_frame_3.setObjectName("picture_frame_3")
        self.picture_frame_4 = QtWidgets.QLabel(self.active_squad)
        self.picture_frame_4.setGeometry(QtCore.QRect(10, 360, 71, 91))
        self.picture_frame_4.setStyleSheet("border: 1px solid black;")
        self.picture_frame_4.setText("")
        self.picture_frame_4.setScaledContents(True)
        self.picture_frame_4.setObjectName("picture_frame_4")
        self.picture_frame_5 = QtWidgets.QLabel(self.active_squad)
        self.picture_frame_5.setGeometry(QtCore.QRect(10, 460, 71, 91))
        self.picture_frame_5.setStyleSheet("border: 1px solid black;")
        self.picture_frame_5.setText("")
        self.picture_frame_5.setScaledContents(True)
        self.picture_frame_5.setObjectName("picture_frame_5")
        self.text_picture_name_2 = QtWidgets.QLineEdit(self.active_squad)
        self.text_picture_name_2.setGeometry(QtCore.QRect(90, 170, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.text_picture_name_2.setFont(font)
        self.text_picture_name_2.setStyleSheet("border: 1px solid black;")
        self.text_picture_name_2.setText("")
        self.text_picture_name_2.setObjectName("text_picture_name_2")
        self.text_picture_name_3 = QtWidgets.QLineEdit(self.active_squad)
        self.text_picture_name_3.setGeometry(QtCore.QRect(90, 270, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.text_picture_name_3.setFont(font)
        self.text_picture_name_3.setStyleSheet("border: 1px solid black;")
        self.text_picture_name_3.setObjectName("text_picture_name_3")
        self.text_picture_name_4 = QtWidgets.QLineEdit(self.active_squad)
        self.text_picture_name_4.setGeometry(QtCore.QRect(90, 370, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.text_picture_name_4.setFont(font)
        self.text_picture_name_4.setStyleSheet("border: 1px solid black;")
        self.text_picture_name_4.setObjectName("text_picture_name_4")
        self.text_picture_name_5 = QtWidgets.QLineEdit(self.active_squad)
        self.text_picture_name_5.setGeometry(QtCore.QRect(90, 470, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.text_picture_name_5.setFont(font)
        self.text_picture_name_5.setStyleSheet("border: 1px solid black;")
        self.text_picture_name_5.setObjectName("text_picture_name_5")
        self.text_picture_name_1 = QtWidgets.QLineEdit(self.active_squad)
        self.text_picture_name_1.setGeometry(QtCore.QRect(90, 70, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.text_picture_name_1.setFont(font)
        self.text_picture_name_1.setStyleSheet("border: 1px solid black;")
        self.text_picture_name_1.setText("")
        self.text_picture_name_1.setObjectName("text_picture_name_1")
        self.club_display = QtWidgets.QScrollArea(self.club)
        self.club_display.setGeometry(QtCore.QRect(330, 10, 751, 561))
        self.club_display.setStyleSheet("border: 1px solid black;")
        self.club_display.setWidgetResizable(True)
        self.club_display.setObjectName("club_display")
        self.scrollAreaWidgetContents_club = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_club.setGeometry(QtCore.QRect(0, 0, 749, 559))
        self.scrollAreaWidgetContents_club.setObjectName("scrollAreaWidgetContents_club")
        self.club_display.setWidget(self.scrollAreaWidgetContents_club)
        self.stacked_widget.addWidget(self.club)
        self.transfer_market = QtWidgets.QWidget()
        self.transfer_market.setObjectName("transfer_market")
        self.transfer_market_frame = QtWidgets.QFrame(self.transfer_market)
        self.transfer_market_frame.setGeometry(QtCore.QRect(20, 10, 1061, 561))
        self.transfer_market_frame.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"}")
        self.transfer_market_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.transfer_market_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.transfer_market_frame.setObjectName("transfer_market_frame")
        self.display_picture = QtWidgets.QLabel(self.transfer_market_frame)
        self.display_picture.setGeometry(QtCore.QRect(60, 40, 181, 201))
        self.display_picture.setStyleSheet("QFrame{\n"
"border: 1px solid black;\n"
"border-radius: 30px;\n"
"}\n"
"\n"
"")
        self.display_picture.setText("")
        self.display_picture.setScaledContents(True)
        self.display_picture.setObjectName("display_picture")
        self.display_market_search = QtWidgets.QLineEdit(self.transfer_market_frame)
        self.display_market_search.setGeometry(QtCore.QRect(62, 250, 181, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.display_market_search.setFont(font)
        self.display_market_search.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.display_market_search.setStyleSheet("QLineEdit{\n"
"border: 1px solid black;\n"
"}")
        self.display_market_search.setClearButtonEnabled(False)
        self.display_market_search.setObjectName("display_market_search")
        self.market_search = QtWidgets.QLabel(self.transfer_market_frame)
        self.market_search.setGeometry(QtCore.QRect(300, 40, 741, 511))
        self.market_search.setStyleSheet("QFrame{\n"
"border: 1px solid black;\n"
"}")
        self.market_search.setText("")
        self.market_search.setObjectName("market_search")
        self.stacked_widget.addWidget(self.transfer_market)
        self.friends_list = QtWidgets.QWidget()
        self.friends_list.setObjectName("friends_list")
        self.friends_list_frame = QtWidgets.QFrame(self.friends_list)
        self.friends_list_frame.setGeometry(QtCore.QRect(20, 50, 521, 511))
        self.friends_list_frame.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"}")
        self.friends_list_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.friends_list_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.friends_list_frame.setObjectName("friends_list_frame")
        self.add_user_frame = QtWidgets.QFrame(self.friends_list)
        self.add_user_frame.setGeometry(QtCore.QRect(580, 10, 501, 181))
        self.add_user_frame.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"}")
        self.add_user_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.add_user_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.add_user_frame.setObjectName("add_user_frame")
        self.add_user_label = QtWidgets.QLabel(self.add_user_frame)
        self.add_user_label.setGeometry(QtCore.QRect(160, 10, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_user_label.setFont(font)
        self.add_user_label.setStyleSheet("QFrame{\n"
"border: 0px solid black;\n"
"}")
        self.add_user_label.setObjectName("add_user_label")
        self.add_user = QtWidgets.QLineEdit(self.add_user_frame)
        self.add_user.setGeometry(QtCore.QRect(50, 51, 401, 111))
        self.add_user.setStyleSheet("QLineEdit{\n"
"border: 1px solid black;\n"
"    font: 20pt \"MS Shell Dlg 2\";\n"
"}\n"
"")
        self.add_user.setText("")
        self.add_user.setObjectName("add_user")
        self.incoming_frame = QtWidgets.QFrame(self.friends_list)
        self.incoming_frame.setGeometry(QtCore.QRect(580, 250, 501, 311))
        self.incoming_frame.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"}")
        self.incoming_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.incoming_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.incoming_frame.setObjectName("incoming_frame")
        self.line = QtWidgets.QFrame(self.incoming_frame)
        self.line.setGeometry(QtCore.QRect(248, 2, 3, 311))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.incoming_label = QtWidgets.QLabel(self.friends_list)
        self.incoming_label.setGeometry(QtCore.QRect(580, 221, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.incoming_label.setFont(font)
        self.incoming_label.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"\n"
"}")
        self.incoming_label.setObjectName("incoming_label")
        self.line_2 = QtWidgets.QFrame(self.friends_list)
        self.line_2.setGeometry(QtCore.QRect(828, 223, 3, 31))
        self.line_2.setStyleSheet("border: 2px solid black;")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.friends_list_label = QtWidgets.QLabel(self.friends_list)
        self.friends_list_label.setGeometry(QtCore.QRect(20, 12, 521, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.friends_list_label.setFont(font)
        self.friends_list_label.setStyleSheet("QLabel{\n"
"border: 2px solid black;\n"
"}")
        self.friends_list_label.setObjectName("friends_list_label")
        self.stacked_widget.addWidget(self.friends_list)
        self.store = QtWidgets.QWidget()
        self.store.setObjectName("store")
        self.pack1 = QtWidgets.QFrame(self.store)
        self.pack1.setGeometry(QtCore.QRect(60, 50, 241, 381))
        self.pack1.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 40px;\n"
"}")
        self.pack1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pack1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pack1.setObjectName("pack1")
        self.pack1_label = QtWidgets.QLabel(self.pack1)
        self.pack1_label.setGeometry(QtCore.QRect(90, 10, 121, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pack1_label.setFont(font)
        self.pack1_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pack1_label.setStyleSheet("border: 0px;\n"
"")
        self.pack1_label.setObjectName("pack1_label")
        self.pack1_text = QtWidgets.QLabel(self.pack1)
        self.pack1_text.setGeometry(QtCore.QRect(20, 128, 201, 171))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pack1_text.setFont(font)
        self.pack1_text.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pack1_text.setStyleSheet("border: 0px;\n"
"")
        self.pack1_text.setObjectName("pack1_text")
        self.purchase_pack1 = QtWidgets.QPushButton(self.store)
        self.purchase_pack1.setGeometry(QtCore.QRect(120, 431, 111, 51))
        self.purchase_pack1.setObjectName("purchase_pack1")
        self.purchase_pack2 = QtWidgets.QPushButton(self.store)
        self.purchase_pack2.setGeometry(QtCore.QRect(490, 430, 111, 51))
        self.purchase_pack2.setObjectName("purchase_pack2")
        self.pack2 = QtWidgets.QFrame(self.store)
        self.pack2.setGeometry(QtCore.QRect(419, 50, 241, 381))
        self.pack2.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 40px;\n"
"}")
        self.pack2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pack2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pack2.setObjectName("pack2")
        self.pack2_label = QtWidgets.QLabel(self.pack2)
        self.pack2_label.setGeometry(QtCore.QRect(90, 10, 71, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pack2_label.setFont(font)
        self.pack2_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pack2_label.setStyleSheet("border: 0px;\n"
"")
        self.pack2_label.setObjectName("pack2_label")
        self.pack2_text = QtWidgets.QLabel(self.pack2)
        self.pack2_text.setGeometry(QtCore.QRect(20, 128, 201, 171))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pack2_text.setFont(font)
        self.pack2_text.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pack2_text.setStyleSheet("border: 0px;\n"
"")
        self.pack2_text.setObjectName("pack2_text")
        self.purchase_pack3 = QtWidgets.QPushButton(self.store)
        self.purchase_pack3.setGeometry(QtCore.QRect(830, 430, 111, 51))
        self.purchase_pack3.setObjectName("purchase_pack3")
        self.pack3 = QtWidgets.QFrame(self.store)
        self.pack3.setGeometry(QtCore.QRect(770, 49, 241, 381))
        self.pack3.setStyleSheet("QFrame{\n"
"border: 2px solid black;\n"
"border-radius: 40px;\n"
"}")
        self.pack3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.pack3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.pack3.setObjectName("pack3")
        self.pack3_label = QtWidgets.QLabel(self.pack3)
        self.pack3_label.setGeometry(QtCore.QRect(90, 10, 61, 71))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pack3_label.setFont(font)
        self.pack3_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pack3_label.setStyleSheet("border: 0px;\n"
"")
        self.pack3_label.setObjectName("pack3_label")
        self.pack3_text = QtWidgets.QLabel(self.pack3)
        self.pack3_text.setGeometry(QtCore.QRect(20, 128, 201, 171))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pack3_text.setFont(font)
        self.pack3_text.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pack3_text.setStyleSheet("border: 0px;\n"
"")
        self.pack3_text.setObjectName("pack3_text")
        self.stacked_widget.addWidget(self.store)
        self.how_to_play_button = QtWidgets.QPushButton(self.main_homepage)
        self.how_to_play_button.setGeometry(QtCore.QRect(450, 80, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.how_to_play_button.setFont(font)
        self.how_to_play_button.setObjectName("how_to_play_button")
        MainWindow.setCentralWidget(self.main_homepage)
        self.actionYes = QtWidgets.QAction(MainWindow)
        self.actionYes.setObjectName("actionYes")
        self.actionNo = QtWidgets.QAction(MainWindow)
        self.actionNo.setObjectName("actionNo")
        self.actionYes_1 = QtWidgets.QAction(MainWindow)
        self.actionYes_1.setObjectName("actionYes_1")
        self.actionNo_1 = QtWidgets.QAction(MainWindow)
        self.actionNo_1.setObjectName("actionNo_1")
        self.actionConfirm_Logout1 = QtWidgets.QAction(MainWindow)
        self.actionConfirm_Logout1.setObjectName("actionConfirm_Logout1")

        self.retranslateUi(MainWindow)
        self.stacked_widget.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.main_page_button_nav.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.main_page_button_nav.setText(_translate("MainWindow", "Main Page"))
        self.club_button_nav.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.club_button_nav.setText(_translate("MainWindow", "Club"))
        self.transfer_market_button_nav.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.transfer_market_button_nav.setText(_translate("MainWindow", "Transfer Market"))
        self.friends_list_button_nav.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.friends_list_button_nav.setText(_translate("MainWindow", "Friends List"))
        self.store_button_nav.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.store_button_nav.setText(_translate("MainWindow", "Store"))
        self.log_out_button_nav.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.log_out_button_nav.setText(_translate("MainWindow", "Log out"))
        self.coin_balance.setText(_translate("MainWindow", "Coin balance:"))
        self.record.setText(_translate("MainWindow", "Record:"))
        self.head_to_head_button.setText(_translate("MainWindow", "Head-To-Head"))
        self.friends_list_button.setText(_translate("MainWindow", "Play Against Your Friends"))
        self.store_button.setText(_translate("MainWindow", "Store"))
        self.club_button.setText(_translate("MainWindow", "Club"))
        self.active_squad_name.setText(_translate("MainWindow", "Active Squad:"))
        self.display_market_search.setPlaceholderText(_translate("MainWindow", "Search For A Player"))
        self.add_user_label.setText(_translate("MainWindow", "Send A Freind Request"))
        self.add_user.setPlaceholderText(_translate("MainWindow", "Type the username here"))
        self.incoming_label.setText(_translate("MainWindow", "Incoming Friend Requests:            Incoming Challenges:"))
        self.friends_list_label.setText(_translate("MainWindow", "Friends List:"))
        self.pack1_label.setText(_translate("MainWindow", "Pack 1"))
        self.pack1_text.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Contains 10 Players <br/></p><p align=\"center\">10,000 Coins</p><p align=\"center\"><br/></p><p><br/></p></body></html>"))
        self.purchase_pack1.setText(_translate("MainWindow", "Buy Pack"))
        self.purchase_pack2.setText(_translate("MainWindow", "Buy Pack"))
        self.pack2_label.setText(_translate("MainWindow", "Pack 2"))
        self.pack2_text.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Contains 30 Players <br/></p><p align=\"center\">25,000 Coins</p><p align=\"center\"><br/></p><p><br/></p></body></html>"))
        self.purchase_pack3.setText(_translate("MainWindow", "Buy Pack"))
        self.pack3_label.setText(_translate("MainWindow", "Pack 3"))
        self.pack3_text.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Contains 50 Players <br/></p><p align=\"center\">45,000 Coins</p><p align=\"center\"><br/></p><p><br/></p></body></html>"))
        self.how_to_play_button.setText(_translate("MainWindow", "How To Play"))
        self.actionYes.setText(_translate("MainWindow", "Yes"))
        self.actionNo.setText(_translate("MainWindow", "No"))
        self.actionYes_1.setText(_translate("MainWindow", "Yes"))
        self.actionNo_1.setText(_translate("MainWindow", "No"))
        self.actionConfirm_Logout1.setText(_translate("MainWindow", "Confirm Logout?"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
