from PyQt5 import QtCore, QtGui, QtWidgets


class PortfoliosForm(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")

        ##-- Кнопка добавления портфеля
        self.add_portfolio = QtWidgets.QPushButton(Dialog)
        self.add_portfolio.setGeometry(QtCore.QRect(550, 0, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_portfolio.setFont(font)
        self.add_portfolio.setStyleSheet("background-color: rgb(255, 0, 255);")
        self.add_portfolio.setObjectName("add")
        self.add_portfolio.setText("Добавить портфель")

        ##-- Кнопка вернуться обратно
        self.back_button = QtWidgets.QPushButton(Dialog)
        self.back_button.setGeometry(QtCore.QRect(220, 500, 101, 41))
        self.back_button.setStyleSheet("background-color:rgb(255,20,20); color: rgb(255,255,255);")
        self.back_button.setObjectName("back")
        self.back_button.setText("Вернуться")

    def retranslateUi(self, Dialog):
        pass

