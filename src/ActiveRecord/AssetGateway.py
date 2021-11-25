import psycopg2
from contextlib import closing



class AssetFinder:
    def __init__(self):
        self.table = 'Assets'
        pass

    def Find(self, id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM {self.table} WHERE epk_id={id}""")
                asset_row = cursor.fetchone()

        Asset = AssetGateway()
        Asset.asset_id = asset_row[0]
        Asset.asset_name = asset_row[1]
        Asset.price = asset_row[2]
        return Asset


class AssetGateway:
    def __init__(self):
        self.asset_id = None
        self.asset_name = None
        self.price = None

        ##-- table
        self.table = 'Assets'
        pass

    def Insert(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""INSERT INTO {self.table} (asset_name, price) 
                                    VALUES ({self.asset_name}, '{self.price}')""")
                conn.commit()
        return

    def Update(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""UPDATE {self.table} SET asset_name='{self.asset_name}' 
                                    WHERE portfolio_id={self.asset_id}""")
                conn.commit()
        return

    def Delete(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""DELETE FROM {self.table} WHERE portfolio_id={self.asset_id}""")
                conn.commit()
        return

