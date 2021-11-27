from PyQt5 import QtCore, QtGui, QtWidgets
from src.Interface.AssetsForm import AssetsForm
from src.ActiveRecord.AssetGateway import AssetFinder
from src.ActiveRecord.PortfolioToAssetsGateway import PortfolioToAssetsGateway, PortfolioToAssetsFinder


class Assett:
    def __init__(self, epk_id, portfolio_id):
        self.epk_id=epk_id
        self.portfolio_id=portfolio_id

    def output_assets(self):
        ##-- ActiveRecord
        ###-- нашли id активов, которые лежат в портфеле
        assetIds = AssetFinder().FindUnlockedAssetsId(self.epk_id, self.portfolio_id)
        assetClassList = list()
        for assetId in assetIds:
            AssetClass = AssetFinder().Find(assetId)
            assetClassList.append(AssetClass)
        return assetClassList

    def del_asset(self, asset_id):
        ##-- ActiveRecord
        PortfolioToAssetsClass = PortfolioToAssetsFinder().FindIdByIds(asset_id, self.portfolio_id)
        PortfolioToAssetsClass.Delete()
        return 1

    def output_blocked_assets(self):
        ##-- ActiveRecord
        lockedAssetsIds = AssetFinder().FindLockedAssetsId(self.epk_id, self.portfolio_id)
        assetClassList = list()
        for lockedAssetsId in lockedAssetsIds:
            AssetClass = AssetFinder().Find(lockedAssetsId)
            assetClassList.append(AssetClass)
        return assetClassList

    def add_to_portfolio(self, asset_id):
        ##-- ActiveRecord
        PortfolioToAssetsClass = PortfolioToAssetsGateway()
        PortfolioToAssetsClass.asset_id = asset_id
        PortfolioToAssetsClass.portfolio_id = self.portfolio_id
        PortfolioToAssetsClass.Insert()
        return 1


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
        ##-- Business logic
        asset = Assett(self.epk_id, self.portfolio_id)
        assetClassList = asset.output_assets()

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
        ##-- Business logic
        asset = Assett(self.epk_id, self.portfolio_id)
        asset_id = self.asset_del_dict[self.sender().objectName()]
        asset.del_asset(asset_id)

        self.close()
        self.Assets = Assets(epk_id=self.epk_id, portfolio_id=self.portfolio_id)
        self.Assets.show()
        pass

    ##-- кнопка "Добавить акцию" - переход к форме добавления акции
    def addForm(self):
        from src.TransactionScript.AssetsList import AssetsListForm
        self.AddForm = AssetsListForm(epk_id=self.epk_id, portfolio_id=self.portfolio_id)
        self.AddForm.show()
        pass

    def back(self):
        from src.TransactionScript.Portfolios import Portfolios
        self.Portfolios = Portfolios(epk_id=self.epk_id)
        self.Portfolios.show()
        self.close()
        pass
    pass

