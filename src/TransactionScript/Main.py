from PyQt5 import QtCore, QtGui, QtWidgets
from src.Interface.LoginForm import Ui_Dialog
import hashlib

from src.ActiveRecord.UserGateway import UserGateway, UserFinder

from src.TransactionScript.Registration import Registration
from src.TransactionScript.Portfolios import Portfolios

# import operator
#
def factorial(n):
    if n < 0:
        raise ValueError("Factorial can't be calculated for negative numbers.")
    if type(n) is float or type(n) is complex:
        raise TypeError("Factorial doesn't use Gamma function.")
    if n == 0:
        return 1
    return factorial(n - 1)


##-- Business logic
class User:
    def __init__(self, login, password, password_repeat=None):
        self.login = login
        self.password = password
        self.password_repeat = password_repeat
        pass

    def check_user(self):
        if self.login == '' and self.password == '':
            return 'Nothing entered'

        if self.check_login() == 'Wrong login':
            return 'Wrong login'
        elif (self.check_password()) == 'Wrong password':
            return 'Wrong password'
        else:
            return self.check_password()
        # enter_login = self.login
        # enter_password = self.password
        # if enter_login == '' and enter_password == '':
        #     return 'Nothing entered'
        # password_hashed = hashlib.md5(enter_password.encode())
        # password_hashed = password_hashed.hexdigest()
        #
        # ##-- Active record
        # usersFinder = UserFinder()
        # logins = usersFinder.FindLogins()
        #
        # if enter_login not in logins:
        #     return 'Wrong login'
        #
        # ##-- Active record
        # user = UserFinder().FindPass(enter_login)
        # password = user.password
        #
        # passwords_hashed = hashlib.md5(password.encode()).hexdigest()
        # if password_hashed not in passwords_hashed:
        #     return 'Wrong password'
        #
        # ##-- Active record
        # epk_id = user.epk_id
        # return epk_id

    def check_login(self):
        enter_login = self.login

        ##-- Active record
        usersFinder = UserFinder()
        logins = usersFinder.FindLogins()

        if enter_login not in logins:
            return 'Wrong login'
        return 1

    def check_password(self):
        enter_login = self.login
        enter_password = self.password
        enter_password_hashed = hashlib.md5(enter_password.encode())
        enter_password_hashed = enter_password_hashed.hexdigest()

        ##-- Active record
        user = UserFinder().FindPass(enter_login)
        user_password = user.password

        user_password_hashed = hashlib.md5(user_password.encode()).hexdigest()
        if enter_password_hashed not in user_password_hashed:
            return 'Wrong password'

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

    def registration(self):
        self.Registration = Registration()
        self.Registration.show()
        # self.close()

