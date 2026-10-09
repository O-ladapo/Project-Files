from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PackWindow(object):
    def setupUi(self, PackWindow):
        PackWindow.setObjectName("PackWindow")
        PackWindow.resize(856, 695)
        PackWindow.setStyleSheet("background-color: rgb(191, 191, 191);")
        self.centralwidget = QtWidgets.QWidget(PackWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.show_packed_cards = QtWidgets.QScrollArea(self.centralwidget)
        self.show_packed_cards.setGeometry(QtCore.QRect(30, 80, 801, 561))
        self.show_packed_cards.setStyleSheet("border: 1px solid black;")
        self.show_packed_cards.setWidgetResizable(True)
        self.show_packed_cards.setObjectName("show_packed_cards")
        self.scrollAreaWidgetContents_show_packed_cards = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_show_packed_cards.setGeometry(QtCore.QRect(0, 0, 799, 559))
        self.scrollAreaWidgetContents_show_packed_cards.setObjectName("scrollAreaWidgetContents_show_packed_cards")
        self.show_packed_cards.setWidget(self.scrollAreaWidgetContents_show_packed_cards)
        PackWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PackWindow)
        QtCore.QMetaObject.connectSlotsByName(PackWindow)

    def retranslateUi(self, PackWindow):
        _translate = QtCore.QCoreApplication.translate
        PackWindow.setWindowTitle(_translate("PackWindow", "MainWindow"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PackWindow = QtWidgets.QMainWindow()
    ui = Ui_PackWindow()
    ui.setupUi(PackWindow)
    PackWindow.show()
    sys.exit(app.exec_())
