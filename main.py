import psycopg2
from contextlib import closing
from PyQt5 import QtCore, QtGui, QtWidgets
from src.LoginForm import Ui_Dialog
from src.RegistrationForm import RegistrationForm
from src.PortfoliosForm import PortfoliosForm
from src.AddPortfolioForm import AddPortfolioForm
import hashlib

global portfolio_name
portfolio_name = None

class AddPortfolio(QtWidgets.QDialog):
    def __init__(self, epk_id:int, parent=None):
        super().__init__(parent)
        self.ui = AddPortfolioForm()
        self.ui.setupUi(self)
        self.epk_id = epk_id
        self.initUI()
        pass

    def initUI(self):
        self.setWindowTitle("AddPortfolio")
        self.ui.add_portfolio.clicked.connect(self.add)
        pass

    def add(self):
        global portfolio_name
        portfolio_name = self.ui.portfolio_nameEdit.text()

        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                if portfolio_name is not None:
                    cursor.execute(f"""
                        INSERT INTO Portfolios (epk_id, portfolio_name) VALUES
                        ({self.epk_id}, '{portfolio_name}')
                        """)

                conn.commit()
        self.close()
        pass
    pass


class Portfolios(QtWidgets.QDialog):
    def __init__(self, login:str, epk_id: int, parent=None):
        super().__init__(parent)
        self.ui = PortfoliosForm()
        self.ui.setupUi(self)
        self.login = login
        self.epk_id = epk_id
        self.initUI()
        pass

    def initUI(self):
        self.setWindowTitle("Portfolios")
        self.output_portfolios()
        self.ui.add_portfolio.clicked.connect(self.add)
        self.ui.update.clicked.connect(self.output_portfolios)

    def output_portfolios(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT portfolio_name FROM Users t1 INNER JOIN Portfolios t2 ON (t1.epk_id=t2.epk_id)
                    WHERE t1.login='{self.login}' 
                """)

                portfolios = cursor.fetchall()
                portfolios = [portfolio[0] for portfolio in portfolios]

                ##-- Вывод портфелей
                for i, portfolio in enumerate(portfolios):
                    ##-- Названия портфелей
                    self.label = QtWidgets.QLabel(self)
                    self.label.setGeometry(QtCore.QRect(0, 80 + i * 100, 171, 51))
                    font = QtGui.QFont()
                    font.setPointSize(16)
                    self.label.setFont(font)
                    self.label.setStyleSheet("color: rgb(0, 0, 0);")
                    self.label.setObjectName(f"portfolio_name_{i}")
                    self.label.setText(portfolio)

                    ##-- Переход к портфелям
                    self.portfolio_btn = QtWidgets.QPushButton(self)
                    self.portfolio_btn.setGeometry(QtCore.QRect(200, 80 + i * 100, 171, 51))
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    self.portfolio_btn.setFont(font)
                    self.portfolio_btn.setStyleSheet("background-color: rgb(0, 170, 0); text-decoration:underline;")
                    self.portfolio_btn.setObjectName(f"portfolio_{i}")
                    self.portfolio_btn.setText("Перейти")

                    cursor.execute(f"""
                        SELECT t2.epk_id FROM Users t1 INNER JOIN Portfolios t2 ON (t1.epk_id=t2.epk_id)
                        WHERE t1.login='{self.login}' 
                    """)

        pass

    def add(self):
        self.Add = AddPortfolio(epk_id=self.epk_id)
        self.Add.show()
        pass
    pass


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
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                login = self.ui.loginEdit.text()
                password_1 = self.ui.passEdit.text()
                password_2 = self.ui.pass_repeatEdit.text()

                cursor.execute("SELECT login FROM Users")
                logins = cursor.fetchall()
                logins = [login[0] for login in logins]

                if login in logins:
                    print("Логин занят")
                    return
                if password_1 != password_2:
                    print("Пароли не совпадают")
                    return

                # cursor.execute(f"INSERT INTO Users (login, pass) VALUES('{login}', '{password_1}')")
                ##-- При создании нового клиента - создается новый портфель
                cursor.execute(f"""
                            with new_client as (
                            INSERT INTO Users (login, pass) VALUES('{login}', '{password_1}')
                              returning epk_id
                            )
                            insert into Portfolios (epk_id, portfolio_name)
                            values
                            (
                              (select epk_id from new_client),
                              'Portfolio_1'
                            );
                            """)

                print("Регистрация прошла успешно")
                self.ui.loginEdit.clear()
                self.ui.passEdit.clear()
                self.ui.pass_repeatEdit.clear()
                conn.commit()
                pass
            pass
        pass

    def back(self):
        self.backWindow = MainForm()
        self.backWindow.show()
        self.close()
    pass



class MainForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.connect()
        self.ui.login_button.clicked.connect(self.check_user)
        self.ui.reg_button.clicked.connect(self.registration)
        # self.disconnect()

    def connect(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"

        ##-- get a connection, if a connect cannot be made an exception will be raised here
        # with closing(psycopg2.connect(conn_string)) as conn:
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor()


    def check_user(self):
        login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if login == '' and password == '':
            return
        password_hashed = hashlib.md5(password.encode())
        password_hashed = password_hashed.hexdigest()
        self.cursor.execute("SELECT login FROM Users")
        logins = self.cursor.fetchall()
        logins = [login[0] for login in logins]

        if login not in logins:
            print("Такого логина нет. Необходимо пройти регистрацию")
            return

        self.cursor.execute(f"SELECT pass FROM Users WHERE login='{login}'")
        passwords = self.cursor.fetchall()
        passwords_hashed = [hashlib.md5(password[0].encode()) for password in passwords]
        passwords_hashed = [password.hexdigest() for password in passwords_hashed]
        if password_hashed not in passwords_hashed:
            print("Неверный пароль")
            return

        print("Вы успешно вошли")


        self.cursor.execute(f"SELECT epk_id FROM Users WHERE login='{login}'")
        epk_id = self.cursor.fetchone()[0]
        ##-- Переход к окну "Портфель"
        self.Portfolio = Portfolios(login=login, epk_id=epk_id)
        self.Portfolio.show()
        self.close()

    def registration(self):
        self.Registration = Registration()
        self.Registration.show()
        # self.close()


    def disconnect(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainForm = MainForm()
    # ui = Ui_Dialog()
    # ui.setupUi(Dialog)
    mainForm.show()
    sys.exit(app.exec_())


# CREATE TABLE Users (
# epk_id SERIAL PRIMARY KEY,
# login TEXT,
# pass TEXT);


# CREATE TABLE Portfolios (
# id SERIAL PRIMARY KEY,
# epk_id INTEGER,
# portfolio_name TEXT,
# FOREIGN KEY (epk_id) REFERENCES Users(id)
# );


# CREATE TABLE Assets(
# assets_id SERIAL PRIMARY KEY,
# asset_name TEXT,
# price Decimal(12,2)
# );


# CREATE TABLE Portfolio_to_Assets (
# id SERIAL PRIMARY KEY,
# portfolio_id INTEGER, assets_id INTEGER,
# FOREIGN KEY(portfolio_id) REFERENCES Portfolios (id),
# FOREIGN KEY(assets_id) REFERENCES Assets (assets_id));
# );
