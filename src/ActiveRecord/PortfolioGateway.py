import psycopg2
from contextlib import closing


class UserPortfoliosFinder:
    def __init__(self):
        self.table = 'Portfolios'
        pass

    def Find(self, epk_id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM {self.table} WHERE epk_id={epk_id}""")
                portfolio_row = cursor.fetchone()

        Portfolio = PortfolioGateway()
        Portfolio.portfolio_id = portfolio_row[0]
        Portfolio.epk_id = portfolio_row[1]
        Portfolio.portfolio_name = portfolio_row[2]
        return Portfolio


class PortfolioFinder:
    def __init__(self):
        self.table = 'Portfolios'
        pass

    def Find(self, id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM {self.table} WHERE portfolio_id={id}""")
                portfolio_row = cursor.fetchone()

        Portfolio = PortfolioGateway()
        Portfolio.portfolio_id = portfolio_row[0]
        Portfolio.epk_id = portfolio_row[1]
        Portfolio.portfolio_name = portfolio_row[2]
        return Portfolio


class PortfolioGateway:
    def __init__(self):
        self.portfolio_id = None
        self.epk_id = None
        self.portfolio_name = None

        ##-- table
        self.table = 'Portfolios'
        pass

    def Insert(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""INSERT INTO {self.table} (epk_id, portfolio_name) 
                                    VALUES ({self.epk_id}, '{self.portfolio_name}')""")
                conn.commit()
        return

    def Update(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""UPDATE {self.table} SET portfolio_name='{self.portfolio_name}' 
                                    WHERE portfolio_id={self.portfolio_id}""")
                conn.commit()
        return

    def Delete(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""DELETE FROM {self.table} WHERE portfolio_id={self.portfolio_id}""")
                conn.commit()
        return
