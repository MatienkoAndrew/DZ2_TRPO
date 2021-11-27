from PyQt5 import QtCore, QtGui, QtWidgets
from src.Interface.PortfoliosForm import PortfoliosForm

from src.ActiveRecord.PortfolioGateway import PortfolioGateway, PortfolioFinder

from src.TransactionScript.AddPortfolio import AddPortfolio

##-- Business logic
class Portfolio:
    def __init__(self, epk_id):
        self.epk_id = epk_id
        pass

    def output_portfolios(self):
        ##-- Active Record
        portfolio_ids = PortfolioFinder().FindUserPortfolios(self.epk_id)
        portfolioClassList = list()
        for portfolio_id in portfolio_ids:
            PortfolioClass = PortfolioFinder().Find(portfolio_id)
            portfolioClassList.append(PortfolioClass)
        return portfolioClassList

    ##-- удаление портфеля по названию
    def del_portfolio(self, portfolio_id):
        ##-- Active Record
        portfolio = PortfolioFinder().Find(portfolio_id)
        try:
            portfolio.Delete()
        except Exception:
            return -1
        return 1

    ##-- обновление портфеля по названию
    def update_portfolio(self, portfolio_id, portfolio_new_name):
        ##-- Active Record
        portfolio = PortfolioFinder().Find(portfolio_id)
        portfolio.portfolio_name = portfolio_new_name
        portfolio.Update()
        return 1

    ##-- добавление нового портфеля
    def add(self, portfolio_name):
        ##-- ActiveRecord
        PortfolioClass = PortfolioGateway()
        PortfolioClass.epk_id = self.epk_id
        PortfolioClass.portfolio_name = portfolio_name
        PortfolioClass.Insert()
        return 1


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
        portfolio_id = self.portfolio_go_dict[self.sender().objectName()]
        self.close()
        from src.TransactionScript.Assets import Assets
        self.Assets = Assets(epk_id=self.epk_id, portfolio_id=portfolio_id)
        self.Assets.show()
        pass

    ##-- удаление портфеля по названию
    def del_portfolio(self):
        ##-- Business logic
        portfolio = Portfolio(self.epk_id)
        portfolio_id = self.portfolio_del_dict[self.sender().objectName()]
        res = portfolio.del_portfolio(portfolio_id)

        if res == -1:
            QtWidgets.QMessageBox.about(self, "Предупреждение", "Невозможно удалить портфель,\n"
                                                                "так как в нем находятся активы.\n"
                                                                "Удалите все активы из портфеля\n"
                                                                "и попробуйте снова")
        self.close()
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()

    ##-- обновление портфеля по названию
    def update_portfolio(self):
        ###-- поиск портфеля по старому названию
        portfolio_id = self.portfolio_update_dict[self.sender().objectName()]

        ###-- Новое название
        ####-- Объектное имя кнопки "Обновить", на которю мы нажимаем
        portfolio_update_object_name = self.sender().objectName()
        idx_portfolio = ''.join(filter(str.isdigit, portfolio_update_object_name))
        ####-- Выводим текст, который отображается в lineEdit у портфеля (после нажатия кнопки обновить)
        portfolio_new_name = self.findChild(QtWidgets.QLineEdit, f"portfolio_name_{idx_portfolio}").text()

        ##-- Business logic
        portfolio = Portfolio(self.epk_id)
        portfolio.update_portfolio(portfolio_id, portfolio_new_name)

        ##-- перезапуск формы
        self.close()
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()

    def output_portfolios(self):
        ##-- Business logic
        portfolio = Portfolio(self.epk_id)
        portfolioClassList = portfolio.output_portfolios()

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
        from src.TransactionScript.Main import MainForm
        self.Main = MainForm()
        self.Main.show()
        self.close()
        pass
    pass
