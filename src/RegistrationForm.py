from PyQt5 import QtCore, QtGui, QtWidgets


class RegistrationForm(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(600, 460)
        Dialog.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(0, 0, 631, 461))
        self.frame.setStyleSheet("background-color: rgb(255, 253, 250);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(230, 80, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(0, 0, 0);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_2.setGeometry(QtCore.QRect(90, 190, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_3.setGeometry(QtCore.QRect(90, 260, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        ##-- Повторение пароля
        self.pass_repeat = QtWidgets.QLabel(self.frame)
        self.pass_repeat.setStyleSheet("color: rgb(0, 0, 0);")
        self.pass_repeat.setGeometry(QtCore.QRect(90, 330, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pass_repeat.setFont(font)
        self.pass_repeat.setObjectName("pass_repeat")

        ##-- Ввод логина
        self.loginEdit = QtWidgets.QLineEdit(self.frame)
        self.loginEdit.setGeometry(QtCore.QRect(260, 190, 231, 31))
        self.loginEdit.setStyleSheet("color: rgb(0, 0, 0);")
        self.loginEdit.setStyleSheet("background-color: rgb(209, 207, 255); color: rgb(0, 0, 0);")
        self.loginEdit.setObjectName("lineEdit")

        ##-- Ввод пароля
        self.passEdit = QtWidgets.QLineEdit(self.frame)
        self.passEdit.setGeometry(QtCore.QRect(260, 260, 231, 31))
        self.passEdit.setStyleSheet("background-color:#d1cfff; color: rgb(0, 0, 0);")
        self.passEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passEdit.setObjectName("lineEdit_2")

        ##-- Повторение пароля
        self.pass_repeatEdit = QtWidgets.QLineEdit(self.frame)
        self.pass_repeatEdit.setGeometry(QtCore.QRect(260, 330, 231, 31))
        self.pass_repeatEdit.setStyleSheet("background-color:#d1cfff; color: rgb(0, 0, 0);")
        self.pass_repeatEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_repeatEdit.setObjectName("lineEdit_2")

        ##-- Кнопка регистрации
        self.reg_button = QtWidgets.QPushButton(self.frame)
        self.reg_button.setGeometry(QtCore.QRect(350, 400, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.reg_button.setFont(font)
        self.reg_button.setStyleSheet("background-color: rgb(0, 170, 0);")
        self.reg_button.setObjectName("pushButton")

        ##-- Кнопка вернуться обратно
        self.back_button = QtWidgets.QPushButton(self.frame)
        self.back_button.setGeometry(QtCore.QRect(220, 400, 101, 41))
        self.back_button.setStyleSheet("background-color:#ffff7f; color: rgb(0,0,0);")
        self.back_button.setObjectName("self.reg_button")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Registration Form"))
        self.label_2.setText(_translate("Dialog", "Введите логин"))
        self.label_3.setText(_translate("Dialog", "Введите пароль"))
        self.pass_repeat.setText(_translate("Dialog", "Повторите пароль"))
        self.reg_button.setText(_translate("Dialog", "Зарегистрироваться"))
        self.back_button.setText(_translate("Dialog", "Back"))

