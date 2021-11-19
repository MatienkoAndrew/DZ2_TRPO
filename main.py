import psycopg2
from contextlib import closing
from PyQt5 import QtCore, QtGui, QtWidgets
from src.LoginForm import Ui_Dialog
from src.RegistrationForm import RegistrationForm
import hashlib

class Registration(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = RegistrationForm()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Registration")
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

            # with conn.cursor() as cursor:
                # conn.cursor will return a cursor object, you can use this cursor to perform queries

                # cursor.execute("DELETE FROM Users WHERE login='Nastya'")
                # cursor.execute("INSERT INTO Users (login, pass) VALUES('Nastya', '1234')")

                ##-- При создании нового клиента - создается новый портфель
                # cursor.execute("""
                #             with new_order as (
                #             insert into Users (login, pass) values ('Nastya', '1234')
                #               returning epk_id
                #             )
                #             insert into Portfolios (epk_id, portfolio_name)
                #             values
                #             (
                #               (select epk_id from new_order),
                #               'test'
                #             );
                #             """)
                #

                # cursor.execute("""UPDATE Users
                #                     SET login='Andrew'
                #                     WHERE login='Nastya'
                #                 """)

                # execute our Query
                # cursor.execute("SELECT * FROM Users")

                # retrieve the records from the database
                # records = cursor.fetchall()

                # print(records)
                # conn.commit()

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
