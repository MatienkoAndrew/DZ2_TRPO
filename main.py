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


# CREATE TABLE Pulse (
# pulse_id SERIAL PRIMARY KEY,
# entered_pulse INT,
# good_pulse INT
# );
