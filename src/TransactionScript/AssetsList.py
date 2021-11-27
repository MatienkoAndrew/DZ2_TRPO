from PyQt5 import QtCore, QtGui, QtWidgets
from src.ActiveRecord.AssetGateway import AssetFinder
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
        from src.TransactionScript.Assets import Assett

        ##-- Business logic
        asset = Assett(self.epk_id, self.portfolio_id)
        assetClassList = asset.output_blocked_assets()

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
        from src.TransactionScript.Assets import Assett

        click_btn = self.sender()
        click_btn_obj_name = click_btn.objectName()
        asset_id = self.asset_dict[click_btn_obj_name]
        click_btn.setEnabled(False)

        ##-- Business logic
        asset = Assett(self.epk_id, self.portfolio_id)
        asset.add_to_portfolio(asset_id)
        pass

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        app = QtGui.QGuiApplication.instance()
        app.closeAllWindows()

        from src.TransactionScript.Assets import Assets
        self.OpenAssetsForm = Assets(epk_id=self.epk_id, portfolio_id=self.portfolio_id)
        self.OpenAssetsForm.show()
        self.close()
        event.accept()
    pass
