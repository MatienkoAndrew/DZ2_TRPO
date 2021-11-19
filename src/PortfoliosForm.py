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


        ##-- Кнопка обновления страницы (для добавления новых портфелей)
        self.update = QtWidgets.QPushButton(Dialog)
        self.update.setGeometry(QtCore.QRect(100, 500, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.update.setFont(font)
        self.update.setStyleSheet("background-color: rgb(255, 0, 255);")
        self.update.setObjectName("add")
        self.update.setText("Обновить")

    def retranslateUi(self, Dialog):
        pass

