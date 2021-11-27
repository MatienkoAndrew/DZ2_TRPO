from PyQt5 import QtCore, QtGui, QtWidgets


class AssetsForm(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Assets")
        Dialog.resize(800, 600)
        Dialog.setStyleSheet("background-color: rgb(255, 255, 255);")

        ##-- Кнопка добавления акции
        self.add_asset = QtWidgets.QPushButton(Dialog)
        self.add_asset.setGeometry(QtCore.QRect(550, 0, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_asset.setFont(font)
        self.add_asset.setStyleSheet("background-color: rgb(255, 26, 26);")
        self.add_asset.setObjectName("add")
        self.add_asset.setText("Добавить акцию")

        ##-- Кнопка вернуться обратно
        self.back_button = QtWidgets.QPushButton(Dialog)
        self.back_button.setGeometry(QtCore.QRect(220, 500, 101, 41))
        self.back_button.setStyleSheet("background-color:rgb(255,20,20); color: rgb(255,255,255);")
        self.back_button.setObjectName("back")
        self.back_button.setText("Вернуться")

    def retranslateUi(self, Dialog):
        pass

