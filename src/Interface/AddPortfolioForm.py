from PyQt5 import QtCore, QtGui, QtWidgets


class AddPortfolioForm(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(300, 200)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")


        ##-- Название
        self.label_portfolio_name = QtWidgets.QLabel(Dialog)
        self.label_portfolio_name.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_portfolio_name.setGeometry(QtCore.QRect(10, 10, 150, 100))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_portfolio_name.setFont(font)
        self.label_portfolio_name.setObjectName("label_portfolio_name")
        self.label_portfolio_name.setText("Название портфеля")

        ##-- Ввод названия
        self.portfolio_nameEdit = QtWidgets.QLineEdit(Dialog)
        self.portfolio_nameEdit.setGeometry(QtCore.QRect(150, 30, 100, 50))
        self.portfolio_nameEdit.setStyleSheet("color: rgb(0, 0, 0);")
        self.portfolio_nameEdit.setStyleSheet("background-color: rgb(209, 207, 255); color: rgb(0, 0, 0);")
        self.portfolio_nameEdit.setObjectName("portfolio_name")


        ##-- Кнопка добавления портфеля
        self.add_portfolio = QtWidgets.QPushButton(Dialog)
        self.add_portfolio.setGeometry(QtCore.QRect(50, 130, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_portfolio.setFont(font)
        self.add_portfolio.setStyleSheet("background-color: rgb(255, 0, 255);")
        self.add_portfolio.setObjectName("add")
        self.add_portfolio.setText("Добавить портфель")

    def retranslateUi(self, Dialog):
        pass

