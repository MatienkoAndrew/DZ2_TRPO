from PyQt5 import QtCore, QtGui, QtWidgets
from src.Interface.AddPortfolioForm import AddPortfolioForm

from src.ActiveRecord.PortfolioGateway import PortfolioGateway, PortfolioFinder


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
        from src.TransactionScript.Portfolios import Portfolios, Portfolio
        ##-- Business logic
        portfolio = Portfolio(self.epk_id)
        portfolio_name = self.ui.portfolio_nameEdit.text()
        portfolio.add(portfolio_name)

        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()
        self.close()
        pass

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        from src.TransactionScript.Portfolios import Portfolios
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()
        self.close()
        event.accept()
    pass

