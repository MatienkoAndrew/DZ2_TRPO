import psycopg2
from contextlib import closing
from PyQt5 import QtCore, QtGui, QtWidgets
from src.LoginForm import Ui_Dialog
from src.RegistrationForm import RegistrationForm
from src.PortfoliosForm import PortfoliosForm
from src.AddPortfolioForm import AddPortfolioForm
from src.AssetsForm import AssetsForm
import hashlib
from peewee import *

from src.ActiveRecord.PortfolioGateway import PortfolioGateway, PortfolioFinder
from src.ActiveRecord.AssetGateway import AssetGateway, AssetFinder
from src.ActiveRecord.UserGateway import UserGateway, UserFinder


class BaseModel(Model):
    class Meta:
        # conn = PostgresqlDatabase('postgres', user='a19053183', password='', host='localhost', port=5432)
        # database = conn
        pass
    pass


class UserRecord(BaseModel):
    def __init__(self):
        self.epk_id = None # AutoField(column_name='epk_id')
        self.login = None # TextField(column_name='login')
        self.password = None # TextField(column_name='pass')

    class Meta:
        table_name = 'Users'

    def select_logins(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT login FROM Users")
                logins = cursor.fetchall()
        logins = [login[0] for login in logins]
        return logins

    def select_password(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT pass FROM Users WHERE login='{self.login}'")
                password = cursor.fetchone()[0]
        return password

    def select_epk_id(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT epk_id FROM Users WHERE login='{self.login}'")
                epk_id = cursor.fetchone()[0]
        return epk_id

    def create_user(self):
        ##-- При создании нового клиента - создается новый портфель
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    with new_client as (
                    INSERT INTO Users (login, pass) VALUES('{self.login}', '{self.password}')
                      returning epk_id
                    )
                    insert into Portfolios (epk_id, portfolio_name)
                    values
                    (
                      (select epk_id from new_client),
                      'Portfolio_1'
                    );
                """)
                conn.commit()
        return
    pass


class PortfolioRecord(BaseModel):
    def __init__(self):
        self.portfolio_id = None #AutoField(column_name='portfolio_id')
        self.epk_id = None #ForeignKeyField(User, column_name='epk_id')
        self.portfolio_name = None #TextField(column_name='portfolio_name')

    class Meta:
        table_name = 'Portfolios'

    ##-- select
    def get_user_portfolios(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                            SELECT portfolio_name FROM Users t1 
                            INNER JOIN Portfolios t2 ON (t1.epk_id=t2.epk_id)
                            WHERE t1.epk_id='{self.epk_id}'
                        """)

                portfolios = cursor.fetchall()
        portfolios = [portfolio[0] for portfolio in portfolios]
        return portfolios

    ##-- select
    def get_portfolio_id(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT portfolio_id 
                    FROM Portfolios 
                    WHERE portfolio_name='{self.portfolio_name}' AND epk_id='{self.epk_id}'
                """)
                portfolio_id = cursor.fetchone()[0]
        return portfolio_id

    ##-- delete
    def delete_portfolio(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                            DELETE FROM Portfolios WHERE portfolio_name='{self.portfolio_name}'
                        """)
                conn.commit()
        return

    ##-- insert
    def insert_portfolio(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                if self.portfolio_name is not None:
                    cursor.execute(f"""
                        INSERT INTO Portfolios (epk_id, portfolio_name) VALUES
                        ({self.epk_id}, '{self.portfolio_name}')
                        """)
                conn.commit()
        return

    ##-- update
    def update_portfolio_name(self, portfolio_new_name):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                if portfolio_new_name.strip() != self.portfolio_name.strip():
                    cursor.execute(f"""
                                UPDATE Portfolios
                                SET portfolio_name = '{portfolio_new_name}'
                                WHERE portfolio_id='{self.portfolio_id}'
                            """)
                    conn.commit()
        return
    pass


class AssetsRecord(BaseModel):
    class Meta:
        table_name = 'Assets'
        pass

    def __init__(self):
        self.asset_id = None # AutoField()
        self.asset_name = None # TextField()
        self.price = None # DecimalField()
        pass

    ##-- select
    def get_assets(self, epk_id, portfolio_id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT t4.asset_name, t4.price
                    FROM
                      Users t1
                    INNER JOIN
                      Portfolios t2
                    ON (t1.epk_id=t2.epk_id)
                    INNER JOIN
                      Portfolio_to_assets t3
                    ON (t2.portfolio_id=t3.portfolio_id)
                    INNER JOIN
                      Assets t4
                    ON (t3.asset_id = t4.asset_id)
                    WHERE t1.epk_id='{epk_id}' 
                            AND t2.portfolio_id='{portfolio_id}'
                """)
                assets = cursor.fetchall()
        return assets

    ##-- select
    def get_asset_id(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT asset_id FROM Assets WHERE asset_name='{self.asset_name}'""")
                asset_id = cursor.fetchone()[0]
        return asset_id

    def get_locked_assets(self, epk_id, portfolio_id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT 
                        asset_name, price
                    FROM 
                        Assets
                    WHERE 
                        asset_name NOT IN 
                            (SELECT 
                                t4.asset_name
                             FROM
                                Users t1
                            INNER JOIN
                                Portfolios t2
                            ON (t1.epk_id=t2.epk_id)
                            INNER JOIN
                                Portfolio_to_assets t3
                            ON (t2.portfolio_id=t3.portfolio_id)
                            INNER JOIN 
                                Assets t4
                            ON (t3.asset_id = t4.asset_id)
                            WHERE 
                                t1.epk_id='{epk_id}' 
                                AND t2.portfolio_id='{portfolio_id}'
                    );
            """)
                assets = cursor.fetchall()
        return assets
    pass


class Portfolio_to_assets_Record(BaseModel):
    class Meta:
        table_name = 'Portfolio_to_assets'
        pass

    def __init__(self):
        self.id_ = None # AutoField()
        self.portfolio_id = None # ForeignKeyField(Portfolio)
        self.asset_id = None # ForeignKeyField(AssetsRecord)
        pass

    ##-- delete
    def delete_asset(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    DELETE FROM Portfolio_to_assets 
                    WHERE asset_id='{self.asset_id}' AND portfolio_id='{self.portfolio_id}'
                """)
                conn.commit()
        return

    ##-- insert
    def create_asset(self, asset_name):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO Portfolio_to_assets (portfolio_id, asset_id)
                    VALUES ('{self.portfolio_id}', (SELECT asset_id FROM Assets WHERE asset_name='{asset_name}'))
                """)
                conn.commit()
        return
    pass


##-- Форма списка Акций
class AssetsListForm(QtWidgets.QDialog):
    def __init__(self, epk_id:int, portfolio_id:int, parent=None):
        super().__init__(parent)
        self.epk_id=epk_id
        self.portfolio_id=portfolio_id
        self.asset_dict = dict()
        self.initUI()

    def initUI(self):
        self.setObjectName("Dialog")
        self.resize(500, 300)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setWindowTitle("AssetsList")
        self.output_assets()

    def output_assets(self):
        AssetClass = AssetsRecord()
        assets = AssetClass.get_locked_assets(self.epk_id, self.portfolio_id)

        ##-- Вывод недоступных акций
        for i, asset in enumerate(assets):
            ##-- Названия актива
            self.assetEdit = QtWidgets.QLineEdit(self)
            self.assetEdit.setGeometry(QtCore.QRect(0, 80 + i * 100, 150, 51))
            self.assetEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.assetEdit.setObjectName(f"asset_name_{i}")
            self.assetEdit.setText(asset[0])
            self.assetEdit.setEnabled(False)

            ##-- Последняя цена актива
            self.priceEdit = QtWidgets.QLineEdit(self)
            self.priceEdit.setGeometry(QtCore.QRect(160, 80 + i * 100, 150, 51))
            self.priceEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.priceEdit.setObjectName(f"price_{i}")
            self.priceEdit.setText(str(asset[1]))
            self.priceEdit.setEnabled(False)

            ##-- Кнопка добавить акцию в портфель
            self.add_btn = QtWidgets.QPushButton(self)
            self.add_btn.setGeometry(QtCore.QRect(320, 80 + i * 100, 150, 51))
            self.add_btn.setStyleSheet("background-color: rgb(0, 170, 0); text-decoration:underline;")
            self.add_btn.setObjectName(f"asset_{i}")
            self.asset_dict[f"asset_{i}"] = asset[0]
            self.add_btn.setText("Добавить")
            self.add_btn.setFocus()
            self.add_btn.clicked.connect(self.add_to_portfolio)
            pass
        pass

    def add_to_portfolio(self):
        click_btn = self.sender()
        click_btn_obj_name = click_btn.objectName()
        asset_name = self.asset_dict[click_btn_obj_name]
        click_btn.setEnabled(False)

        ##-- ActiveRecord
        Portfolio_to_assets_Class = Portfolio_to_assets_Record()
        Portfolio_to_assets_Class.portfolio_id = self.portfolio_id
        Portfolio_to_assets_Class.create_asset(asset_name)
        pass

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        app = QtGui.QGuiApplication.instance()
        app.closeAllWindows()
        self.OpenAssetsForm = Assets(epk_id=self.epk_id, portfolio_id=self.portfolio_id)
        self.OpenAssetsForm.show()
        self.close()
        event.accept()
    pass


##-- Форма Акции
class Assets(QtWidgets.QDialog):
    def __init__(self, epk_id:int, portfolio_id:int, parent=None):
        super().__init__(parent)
        self.ui = AssetsForm()
        self.ui.setupUi(self)
        self.epk_id=epk_id
        self.portfolio_id=portfolio_id
        self.asset_del_dict = dict()
        self.initUI()
        pass

    def initUI(self):
        self.setWindowTitle("Assets")
        self.output_assets()
        self.ui.add_asset.clicked.connect(self.addForm)
        self.ui.back_button.clicked.connect(self.back)

    def output_assets(self):
        ##-- ActiveRecord
        AssetClass = AssetsRecord()
        assets = AssetClass.get_assets(self.epk_id, self.portfolio_id)

        ##-- Вывод акций в портфеле
        for i, asset in enumerate(assets):
            ##-- Названия актива
            self.assetEdit = QtWidgets.QLineEdit(self)
            self.assetEdit.setGeometry(QtCore.QRect(0, 80 + i * 100, 150, 51))
            self.assetEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.assetEdit.setObjectName(f"portfolio_name_{i}")
            self.assetEdit.setText(asset[0])
            self.assetEdit.setEnabled(False)

            ##-- Последняя цена актива
            self.priceEdit = QtWidgets.QLineEdit(self)
            self.priceEdit.setGeometry(QtCore.QRect(160, 80 + i * 100, 150, 51))
            self.priceEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.priceEdit.setObjectName(f"portfolio_name_{i}")
            self.priceEdit.setText(str(asset[1]))
            self.priceEdit.setEnabled(False)

            ##-- Кнопка удаления актива из портфеля
            self.asset_del = QtWidgets.QPushButton(self)
            self.asset_del.setGeometry(QtCore.QRect(320, 80 + i * 100, 150, 51))
            self.asset_del.setStyleSheet("background-color: rgb(255, 20, 20); text-decoration:underline;")
            self.asset_del.setObjectName(f"asset_del_{i}")
            self.asset_del_dict[f"asset_del_{i}"] = asset[0]
            self.asset_del.setText("Удалить")
            self.asset_del.clicked.connect(self.del_asset)
            pass
        pass

    def del_asset(self):
        ##-- ActiveRecord
        AssetClass = AssetsRecord()
        AssetClass.asset_name = self.asset_del_dict[self.sender().objectName()]
        asset_id = AssetClass.get_asset_id()

        ##-- ActiveRecord
        Portfolio_to_assets_Class = Portfolio_to_assets_Record()
        Portfolio_to_assets_Class.asset_id = asset_id
        Portfolio_to_assets_Class.portfolio_id = self.portfolio_id
        Portfolio_to_assets_Class.delete_asset()

        self.close()
        self.Assets = Assets(epk_id=self.epk_id, portfolio_id=self.portfolio_id)
        self.Assets.show()

        pass

    ##-- кнопка "Добавить акцию" - переход к форме добавления акции
    def addForm(self):
        self.AddForm = AssetsListForm(epk_id=self.epk_id, portfolio_id=self.portfolio_id)
        self.AddForm.show()
        pass

    def back(self):
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()
        self.close()
        pass
    pass


##-- Форма добавления портфеля
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
        portfolio_class = PortfolioRecord()
        portfolio_class.epk_id = self.epk_id
        portfolio_class.portfolio_name = self.ui.portfolio_nameEdit.text()
        portfolio_class.insert_portfolio()
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()
        self.close()
        pass

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()
        self.close()
        event.accept()
    pass


##-- Форма Портфели
class Portfolios(QtWidgets.QDialog):
    def __init__(self, epk_id: int, parent=None):
        super().__init__(parent)
        self.ui = PortfoliosForm()
        self.ui.setupUi(self)
        self.epk_id = epk_id
        self.portfolio_del_dict = dict()
        self.portfolio_update_dict = dict()
        self.portfolio_go_dict = dict()
        self.initUI()
        pass

    def initUI(self):
        self.setWindowTitle("Portfolios")
        self.output_portfolios()
        self.ui.add_portfolio.clicked.connect(self.add)
        self.ui.back_button.clicked.connect(self.back)

    ##-- переход к портфелю
    def go_portfolio(self):
        ##-- Active Record
        portfolio_class = PortfolioRecord()
        portfolio_class.epk_id = self.epk_id
        portfolio_class.portfolio_name = self.portfolio_go_dict[self.sender().objectName()]
        portfolio_id = portfolio_class.get_portfolio_id()

        self.close()
        self.Assets = Assets(epk_id=self.epk_id, portfolio_id=portfolio_id)
        self.Assets.show()
        pass

    ##-- удаление портфеля по названию
    def del_portfolio(self):
        ##-- Active Record
        portfolio_class = PortfolioRecord()
        portfolio_class.portfolio_name = self.portfolio_del_dict[self.sender().objectName()]
        portfolio_class.delete_portfolio()
        self.close()
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()

    ##-- обновление портфеля по названию
    def update_portfolio(self):
        ##-- Active Record
        portfolio_class = PortfolioRecord()
        portfolio_class.epk_id = self.epk_id
        portfolio_class.portfolio_name = self.portfolio_update_dict[self.sender().objectName()]
        portfolio_id = portfolio_class.get_portfolio_id()
        portfolio_class.portfolio_id = portfolio_id
        ##-- Объектное имя кнопки "Обновить", на которю мы нажимаем
        portfolio_update_object_name = self.sender().objectName()
        idx_portfolio = ''.join(filter(str.isdigit, portfolio_update_object_name))
        ##-- Выводим текст, который отображается в lineEdit у портфеля (после нажатия кнопки обновить)
        portfolio_new_name = self.findChild(QtWidgets.QLineEdit, f"portfolio_name_{idx_portfolio}").text()
        portfolio_class.update_portfolio_name(portfolio_new_name)

        ##-- перезапуск формы
        self.close()
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()

    def output_portfolios(self):
        ##-- Active Record
        portfolios_class = PortfolioRecord()
        portfolios_class.epk_id = self.epk_id
        portfolios = portfolios_class.get_user_portfolios()

        ##-- Вывод портфелей
        for i, portfolio in enumerate(portfolios):
            ##-- Названия портфелей
            self.portfolioEdit = QtWidgets.QLineEdit(self)
            self.portfolioEdit.setGeometry(QtCore.QRect(0, 80 + i * 100, 150, 51))
            self.portfolioEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.portfolioEdit.setObjectName(f"portfolio_name_{i}")
            self.portfolioEdit.setText(portfolio)

            ##-- Обновление названий
            self.portfolio_update = QtWidgets.QPushButton(self)
            self.portfolio_update.setGeometry(QtCore.QRect(160, 80 + i * 100, 100, 51))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.portfolio_update.setFont(font)
            self.portfolio_update.setStyleSheet("background-color: rgb(0, 100, 0); text-decoration:underline;")
            self.portfolio_update.setObjectName(f"portfolio_update_{i}")
            self.portfolio_update_dict[f"portfolio_update_{i}"] = portfolio
            self.portfolio_update.setText("Обновить")
            self.portfolio_update.clicked.connect(self.update_portfolio)

            ##-- Переход к портфелям
            self.portfolio_btn = QtWidgets.QPushButton(self)
            self.portfolio_btn.setGeometry(QtCore.QRect(270, 80 + i * 100, 171, 51))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.portfolio_btn.setFont(font)
            self.portfolio_btn.setStyleSheet("background-color: rgb(0, 170, 0); text-decoration:underline;")
            self.portfolio_btn.setObjectName(f"portfolio_{i}")
            self.portfolio_go_dict[f"portfolio_{i}"] = portfolio
            self.portfolio_btn.setText("Перейти")
            self.portfolio_btn.setFocus()
            self.portfolio_btn.clicked.connect(self.go_portfolio)

            ##-- Кнопка удаления
            self.portfolio_del = QtWidgets.QPushButton(self)
            self.portfolio_del.setGeometry(QtCore.QRect(450, 80 + i * 100, 171, 51))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.portfolio_del.setFont(font)
            self.portfolio_del.setStyleSheet("background-color: rgb(255, 0, 0); text-decoration:underline;")
            self.portfolio_del.setObjectName(f"portfolio_del_{i}")
            self.portfolio_del_dict[f"portfolio_del_{i}"] = portfolio
            self.portfolio_del.setText("Удалить")
            self.portfolio_del.clicked.connect(self.del_portfolio)
            pass
        pass

    def add(self):
        self.Add = AddPortfolio(epk_id=self.epk_id)
        self.Add.show()
        self.close()
        pass

    def back(self):
        self.Main = MainForm()
        self.Main.show()
        self.close()
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
        enter_login = self.ui.loginEdit.text()
        password_1 = self.ui.passEdit.text()
        password_2 = self.ui.pass_repeatEdit.text()

        ##-- Active record
        User_class = UserRecord()
        logins = User_class.select_logins()

        if enter_login in logins:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Логин занят")
            return
        if password_1 != password_2:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Пароли не совпадают")
            return

        ##-- Active record
        User_class.login = enter_login
        User_class.password = password_1
        User_class.create_user()

        QtWidgets.QMessageBox.about(self, "Предупреждение", "Регистрация прошла успешно")
        self.ui.loginEdit.clear()
        self.ui.passEdit.clear()
        self.ui.pass_repeatEdit.clear()
        self.close()
        pass

    def back(self):
        self.backWindow = MainForm()
        self.backWindow.show()
        self.close()
    pass






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
        enter_login = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if enter_login == '' and password == '':
            return
        password_hashed = hashlib.md5(password.encode())
        password_hashed = password_hashed.hexdigest()

        ##-- Active record
        User_class = UserRecord()
        logins = User_class.select_logins()
        if enter_login not in logins:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Такого логина нет. Необходимо пройти регистрацию")
            return

        ##-- Active record
        User_class.login = enter_login
        password = User_class.select_password()

        passwords_hashed = hashlib.md5(password.encode()).hexdigest()
        if password_hashed not in passwords_hashed:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Неверный пароль")
            return

        ##-- Active record
        epk_id = User_class.select_epk_id()


        # finder = PortfolioFinder()
        # PortfolioExampler = finder.Find(1)
        # PortfolioExampler.portfolio_name = "I change the name"
        # PortfolioExampler.Update()

        # PortfolioNew = PortfolioGateway()
        # PortfolioNew.epk_id = 1
        # PortfolioNew.portfolio_name = 'New portfolio'
        # PortfolioNew.Insert()








        ##-- Переход к окну "Портфель"
        self.Portfolio = Portfolios(epk_id=epk_id)
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
# pass TEXT
# );


# CREATE TABLE Portfolios (
# portfolio_id SERIAL PRIMARY KEY,
# epk_id INTEGER,
# portfolio_name TEXT,
# FOREIGN KEY (epk_id) REFERENCES Users(id)
# );


# CREATE TABLE Assets(
# asset_id SERIAL PRIMARY KEY,
# asset_name TEXT,
# price Decimal(12,2)
# );


# CREATE TABLE Portfolio_to_Assets (
# id SERIAL PRIMARY KEY,
# portfolio_id INTEGER,
# asset_id INTEGER,
# FOREIGN KEY(portfolio_id) REFERENCES Portfolios (portfolio_id),
# FOREIGN KEY(asset_id) REFERENCES Assets (asset_id));
# );

##--

# SELECT *
# FROM
#   Users t1
# INNER JOIN
#   Portfolios t2
# ON (t1.epk_id=t2.epk_id)
# INNER JOIN
#   Portfolio_to_assets t3
# ON (t2.portfolio_id=t3.portfolio_id)
# INNER JOIN
#   Assets t4
# ON (t3.asset_id = t4.asset_id);
