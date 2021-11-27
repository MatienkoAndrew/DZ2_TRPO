from PyQt5 import QtCore, QtGui, QtWidgets
from src.Interface.RegistrationForm import RegistrationForm
from src.ActiveRecord.UserGateway import UserGateway, UserFinder


class Registration(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = RegistrationForm()
        self.ui.setupUi(self)
        self.backWindow = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Registration")
        self.ui.reg_button.clicked.connect(self.registration)
        self.ui.back_button.clicked.connect(self.back)
    pass

    def registration(self):
        from src.TransactionScript.Main import User

        enter_login = self.ui.loginEdit.text()
        password_1 = self.ui.passEdit.text()
        password_2 = self.ui.pass_repeatEdit.text()

        ##-- Business logic
        user = User(enter_login, password_1, password_2)
        res = user.registration()

        if res == 0:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Логин занят")
            return
        if res == -1:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Пароли не совпадают")
            return

        QtWidgets.QMessageBox.about(self, "Предупреждение", "Регистрация прошла успешно")
        self.ui.loginEdit.clear()
        self.ui.passEdit.clear()
        self.ui.pass_repeatEdit.clear()
        self.close()
        pass

    def back(self):
        from src.TransactionScript.Main import MainForm
        self.backWindow = MainForm()
        self.backWindow.show()
        self.close()
    pass

