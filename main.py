from PyQt5 import QtCore, QtGui, QtWidgets
from src.LoginForm import Ui_Dialog
from src.RegistrationForm import RegistrationForm
from src.PortfoliosForm import PortfoliosForm
from src.AddPortfolioForm import AddPortfolioForm
from src.AssetsForm import AssetsForm
import hashlib

from src.ActiveRecord.PortfolioGateway import PortfolioGateway, PortfolioFinder
from src.ActiveRecord.AssetGateway import AssetGateway, AssetFinder
from src.ActiveRecord.UserGateway import UserGateway, UserFinder
from src.ActiveRecord.PortfolioToAssetsGateway import PortfolioToAssetsGateway, PortfolioToAssetsFinder



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
        ##-- ActiveRecord
        lockedAssetsIds = AssetFinder().FindLockedAssetsId(self.epk_id, self.portfolio_id)
        assetClassList = list()
        for lockedAssetsId in lockedAssetsIds:
            AssetClass = AssetFinder().Find(lockedAssetsId)
            assetClassList.append(AssetClass)

        ##-- Вывод недоступных акций
        for i, AssetClass in enumerate(assetClassList):
            ##-- Названия актива
            self.assetEdit = QtWidgets.QLineEdit(self)
            self.assetEdit.setGeometry(QtCore.QRect(0, 80 + i * 100, 150, 51))
            self.assetEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.assetEdit.setObjectName(f"asset_name_{AssetClass.asset_id}")
            self.assetEdit.setText(AssetClass.asset_name)
            self.assetEdit.setEnabled(False)

            ##-- Последняя цена актива
            self.priceEdit = QtWidgets.QLineEdit(self)
            self.priceEdit.setGeometry(QtCore.QRect(160, 80 + i * 100, 150, 51))
            self.priceEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.priceEdit.setObjectName(f"price_{AssetClass.asset_id}")
            self.priceEdit.setText(str(AssetClass.price))
            self.priceEdit.setEnabled(False)

            ##-- Кнопка добавить акцию в портфель
            self.add_btn = QtWidgets.QPushButton(self)
            self.add_btn.setGeometry(QtCore.QRect(320, 80 + i * 100, 150, 51))
            self.add_btn.setStyleSheet("background-color: rgb(0, 170, 0); text-decoration:underline;")
            self.add_btn.setObjectName(f"asset_{AssetClass.asset_id}")
            self.asset_dict[f"asset_{AssetClass.asset_id}"] = AssetClass.asset_id
            self.add_btn.setText("Добавить")
            self.add_btn.setFocus()
            self.add_btn.clicked.connect(self.add_to_portfolio)
            pass
        pass

    def add_to_portfolio(self):
        click_btn = self.sender()
        click_btn_obj_name = click_btn.objectName()
        asset_id = self.asset_dict[click_btn_obj_name]
        click_btn.setEnabled(False)

        ##-- ActiveRecord
        PortfolioToAssetsClass = PortfolioToAssetsGateway()
        PortfolioToAssetsClass.asset_id = asset_id
        PortfolioToAssetsClass.portfolio_id = self.portfolio_id
        PortfolioToAssetsClass.Insert()
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
        ###-- нашли id активов, которые лежат в портфеле
        assetIds = AssetFinder().FindUnlockedAssetsId(self.epk_id, self.portfolio_id)
        assetClassList = list()
        for assetId in assetIds:
            AssetClass = AssetFinder().Find(assetId)
            assetClassList.append(AssetClass)

        ##-- Вывод акций в портфеле
        for i, Asset in enumerate(assetClassList):
            ##-- Названия актива
            self.assetEdit = QtWidgets.QLineEdit(self)
            self.assetEdit.setGeometry(QtCore.QRect(0, 80 + i * 100, 150, 51))
            self.assetEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.assetEdit.setObjectName(f"asset_name_{Asset.asset_id}")
            self.assetEdit.setText(Asset.asset_name)
            self.assetEdit.setEnabled(False)

            ##-- Последняя цена актива
            self.priceEdit = QtWidgets.QLineEdit(self)
            self.priceEdit.setGeometry(QtCore.QRect(160, 80 + i * 100, 150, 51))
            self.priceEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.priceEdit.setObjectName(f"asset_name_{Asset.asset_id}")
            self.priceEdit.setText(str(Asset.price))
            self.priceEdit.setEnabled(False)

            ##-- Кнопка удаления актива из портфеля
            self.asset_del = QtWidgets.QPushButton(self)
            self.asset_del.setGeometry(QtCore.QRect(320, 80 + i * 100, 150, 51))
            self.asset_del.setStyleSheet("background-color: rgb(255, 20, 20); text-decoration:underline;")
            self.asset_del.setObjectName(f"asset_del_{Asset.asset_id}")
            self.asset_del_dict[f"asset_del_{Asset.asset_id}"] = Asset.asset_id
            self.asset_del.setText("Удалить")
            self.asset_del.clicked.connect(self.del_asset)
            pass
        pass

    def del_asset(self):
        ##-- ActiveRecord
        asset_id = self.asset_del_dict[self.sender().objectName()]
        PortfolioToAssetsClass = PortfolioToAssetsFinder().FindIdByIds(asset_id, self.portfolio_id)
        PortfolioToAssetsClass.Delete()

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
        ##-- ActiveRecord
        PortfolioClass = PortfolioGateway()
        PortfolioClass.epk_id = self.epk_id
        PortfolioClass.portfolio_name = self.ui.portfolio_nameEdit.text()
        PortfolioClass.Insert()

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
        portfolio_id = self.portfolio_go_dict[self.sender().objectName()]

        self.close()
        self.Assets = Assets(epk_id=self.epk_id, portfolio_id=portfolio_id)
        self.Assets.show()
        pass

    ##-- удаление портфеля по названию
    def del_portfolio(self):
        ##-- Active Record
        portfolio_id = self.portfolio_del_dict[self.sender().objectName()]
        PortfolioClass = PortfolioFinder().Find(portfolio_id)
        try:
            PortfolioClass.Delete()
        except Exception:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Невозможно удалить портфель,\n"
                                                                "так как в нем находятся активы.\n"
                                                                "Удалите все активы из портфеля\n"
                                                                "и попробуйте снова")
        self.close()
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()

    ##-- обновление портфеля по названию
    def update_portfolio(self):
        ##-- Active Record
        ###-- поиск портфеля по старому названию
        portfolio_id = self.portfolio_update_dict[self.sender().objectName()]
        PortfolioClass = PortfolioFinder().Find(portfolio_id)

        ###-- Новое название

        ####-- Объектное имя кнопки "Обновить", на которю мы нажимаем
        portfolio_update_object_name = self.sender().objectName()
        idx_portfolio = ''.join(filter(str.isdigit, portfolio_update_object_name))
        ####-- Выводим текст, который отображается в lineEdit у портфеля (после нажатия кнопки обновить)
        portfolio_new_name = self.findChild(QtWidgets.QLineEdit, f"portfolio_name_{idx_portfolio}").text()
        PortfolioClass.portfolio_name = portfolio_new_name
        PortfolioClass.Update()

        ##-- перезапуск формы
        self.close()
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()

    def output_portfolios(self):
        ##-- Active Record
        portfolio_ids = PortfolioFinder().FindUserPortfolios(self.epk_id)
        portfolioClassList = list()
        for portfolio_id in portfolio_ids:
            PortfolioClass = PortfolioFinder().Find(portfolio_id)
            portfolioClassList.append(PortfolioClass)

        ##-- Вывод портфелей
        for i, PortfolioClass in enumerate(portfolioClassList):
            ##-- Названия портфелей
            self.portfolioEdit = QtWidgets.QLineEdit(self)
            self.portfolioEdit.setGeometry(QtCore.QRect(0, 80 + i * 100, 150, 51))
            self.portfolioEdit.setStyleSheet("color: rgb(0, 0, 0);")
            self.portfolioEdit.setObjectName(f"portfolio_name_{PortfolioClass.portfolio_id}")
            self.portfolioEdit.setText(PortfolioClass.portfolio_name)

            ##-- Обновление названий
            self.portfolio_update = QtWidgets.QPushButton(self)
            self.portfolio_update.setGeometry(QtCore.QRect(160, 80 + i * 100, 100, 51))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.portfolio_update.setFont(font)
            self.portfolio_update.setStyleSheet("background-color: rgb(0, 100, 0); text-decoration:underline;")
            self.portfolio_update.setObjectName(f"portfolio_update_{PortfolioClass.portfolio_id}")
            self.portfolio_update_dict[f"portfolio_update_{PortfolioClass.portfolio_id}"] = PortfolioClass.portfolio_id
            self.portfolio_update.setText("Обновить")
            self.portfolio_update.clicked.connect(self.update_portfolio)

            ##-- Переход к портфелям
            self.portfolio_btn = QtWidgets.QPushButton(self)
            self.portfolio_btn.setGeometry(QtCore.QRect(270, 80 + i * 100, 171, 51))
            font = QtGui.QFont()
            font.setPointSize(14)
            self.portfolio_btn.setFont(font)
            self.portfolio_btn.setStyleSheet("background-color: rgb(0, 170, 0); text-decoration:underline;")
            self.portfolio_btn.setObjectName(f"portfolio_{PortfolioClass.portfolio_id}")
            self.portfolio_go_dict[f"portfolio_{PortfolioClass.portfolio_id}"] = PortfolioClass.portfolio_id
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
            self.portfolio_del.setObjectName(f"portfolio_del_{PortfolioClass.portfolio_id}")
            self.portfolio_del_dict[f"portfolio_del_{PortfolioClass.portfolio_id}"] = PortfolioClass.portfolio_id
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
        logins = UserFinder().FindLogins()

        if enter_login in logins:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Логин занят")
            return
        if password_1 != password_2:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Пароли не совпадают")
            return

        ##-- Active record
        User = UserGateway()
        User.login = enter_login
        User.password = password_1
        User.Insert()

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
        Users = UserFinder()
        logins = Users.FindLogins()

        if enter_login not in logins:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Такого логина нет. Необходимо пройти регистрацию")
            return

        ##-- Active record
        User = UserFinder().FindPass(enter_login)
        password = User.password

        passwords_hashed = hashlib.md5(password.encode()).hexdigest()
        if password_hashed not in passwords_hashed:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Неверный пароль")
            return

        ##-- Active record
        epk_id = User.epk_id

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
