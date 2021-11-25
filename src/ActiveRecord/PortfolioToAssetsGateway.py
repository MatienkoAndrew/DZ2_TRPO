import psycopg2
from contextlib import closing



class PortfolioToAssetsFinder:
    def __init__(self):
        self.table = 'Portfolio_to_assets'
        pass

    def Find(self, id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM {self.table} WHERE id={id}""")
                row = cursor.fetchone()

        PortfolioToAssets = PortfolioToAssetsGateway()
        PortfolioToAssets.id = row[0]
        PortfolioToAssets.portfolio_id = row[1]
        PortfolioToAssets.asset_id = row[2]
        return PortfolioToAssets


    def FindIdByIds(self, asset_id, portfolio_id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM {self.table} WHERE asset_id={asset_id} AND portfolio_id={portfolio_id}""")
                row = cursor.fetchone()

        PortfolioToAssets = PortfolioToAssetsGateway()
        PortfolioToAssets.id = row[0]
        PortfolioToAssets.portfolio_id = row[1]
        PortfolioToAssets.asset_id = row[2]
        return PortfolioToAssets


class PortfolioToAssetsGateway:
    def __init__(self):
        self.id = None
        self.portfolio_id = None
        self.asset_id = None

        ##-- table
        self.table = 'Portfolio_to_assets'
        pass

    def Insert(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""INSERT INTO {self.table} (portfolio_id, asset_id) 
                                    VALUES ({self.portfolio_id}, '{self.asset_id}')""")
                conn.commit()
        return

    def Delete(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""DELETE FROM {self.table} WHERE id={self.id}""")
                conn.commit()
        return

