from PyQt5 import QtCore, QtGui, QtWidgets
from src.Interface.LoginForm import Ui_Dialog
from src.Interface.RegistrationForm import RegistrationForm
from src.Interface.PortfoliosForm import PortfoliosForm
from src.Interface.AddPortfolioForm import AddPortfolioForm
from src.Interface.AssetsForm import AssetsForm
import hashlib

from src.ActiveRecord.PortfolioGateway import PortfolioGateway, PortfolioFinder
from src.ActiveRecord.AssetGateway import AssetFinder
from src.ActiveRecord.UserGateway import UserGateway, UserFinder
from src.ActiveRecord.PortfolioToAssetsGateway import PortfolioToAssetsGateway, PortfolioToAssetsFinder

from src.TransactionScript.Main import MainForm


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
