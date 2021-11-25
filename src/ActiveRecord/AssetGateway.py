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
                cursor.execute(f"""SELECT * FROM {self.table} WHERE asset_id={id}""")
                asset_row = cursor.fetchone()

        Asset = AssetGateway()
        Asset.asset_id = asset_row[0]
        Asset.asset_name = asset_row[1]
        Asset.price = asset_row[2]
        return Asset

    def FindUnlockedAssetsId(self, epk_id, portfolio_id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT t4.asset_id
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
                asset_rows = cursor.fetchall()
        asset_rows = [asset_row[0] for asset_row in asset_rows]
        return asset_rows

    def FindLockedAssetsId(self, epk_id, portfolio_id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""
                    SELECT 
                        asset_id
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
                asset_rows = cursor.fetchall()
        asset_rows = [asset_row[0] for asset_row in asset_rows]
        return asset_rows


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
                                    WHERE asset_id={self.asset_id}""")
                conn.commit()
        return

    def Delete(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""DELETE FROM {self.table} WHERE asset_id={self.asset_id}""")
                conn.commit()
        return

