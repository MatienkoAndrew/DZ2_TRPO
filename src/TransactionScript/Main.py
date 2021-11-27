from PyQt5 import QtCore, QtGui, QtWidgets
from src.Interface.LoginForm import Ui_Dialog
import hashlib

from src.ActiveRecord.UserGateway import UserGateway, UserFinder

from src.TransactionScript.Registration import Registration
from src.TransactionScript.Portfolios import Portfolios


##-- Business logic
class User:
    def __init__(self, login, password, password_repeat=None):
        self.login = login
        self.password = password
        self.password_repeat = password_repeat
        pass

    def check_user(self):
        enter_login = self.login
        password = self.password
        if enter_login == '' and password == '':
            return 'Nothing entered'
        password_hashed = hashlib.md5(password.encode())
        password_hashed = password_hashed.hexdigest()

        ##-- Active record
        usersFinder = UserFinder()
        logins = usersFinder.FindLogins()

        if enter_login not in logins:
            return 'Wrong login'

        ##-- Active record
        user = UserFinder().FindPass(enter_login)
        password = user.password

        passwords_hashed = hashlib.md5(password.encode()).hexdigest()
        if password_hashed not in passwords_hashed:
            return 'Wrong password'

        ##-- Active record
        epk_id = user.epk_id
        return epk_id


    def registration(self):
        enter_login = self.login
        password_1 = self.password
        password_2 = self.password_repeat

        ##-- Active record
        logins = UserFinder().FindLogins()

        if enter_login in logins:
            return 0
        if password_1 != password_2:
            return -1

        ##-- Active record
        user = UserGateway()
        user.login = enter_login
        user.password = password_1
        user.Insert()
        return 1


##-- Главное окно
class MainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.ui.login_button.clicked.connect(self.check_user)
        self.ui.reg_button.clicked.connect(self.registration)

    def check_user(self):
        ##-- Business logic
        user = User(self.ui.lineEdit.text(), self.ui.lineEdit_2.text())
        res = user.check_user()

        if res == 'Wrong login':
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Такого логина нет. Необходимо пройти регистрацию")
            return
        elif res == 'Wrong password':
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Неверный пароль")
            return
        elif res == 'Nothing entered':
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Ничего невведено")
            return
        else:
            ##-- Переход к окну "Портфель"
            self.Portfolio = Portfolios(epk_id=res)
            self.Portfolio.show()
            self.close()

        #
        # enter_login = self.ui.lineEdit.text()
        # password = self.ui.lineEdit_2.text()
        # if enter_login == '' and password == '':
        #     return
        # password_hashed = hashlib.md5(password.encode())
        # password_hashed = password_hashed.hexdigest()
        #
        # ##-- Active record
        # Users = UserFinder()
        # logins = Users.FindLogins()
        #
        # if enter_login not in logins:
        #     QtWidgets.QMessageBox.about(self, "Предупреждение", "Такого логина нет. Необходимо пройти регистрацию")
        #     return
        #
        # ##-- Active record
        # User = UserFinder().FindPass(enter_login)
        # password = User.password
        #
        # passwords_hashed = hashlib.md5(password.encode()).hexdigest()
        # if password_hashed not in passwords_hashed:
        #     QtWidgets.QMessageBox.about(self, "Предупреждение", "Неверный пароль")
        #     return
        #
        # ##-- Active record
        # epk_id = User.epk_id
        #
        ##-- Переход к окну "Портфель"
        # self.Portfolio = Portfolios(epk_id=epk_id)
        # self.Portfolio.show()
        # self.close()

    def registration(self):
        self.Registration = Registration()
        self.Registration.show()
        # self.close()

