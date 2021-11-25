import psycopg2
from contextlib import closing



class UserFinder:
    def __init__(self):
        self.table = 'Users'
        pass

    def Find(self, id):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""SELECT * FROM {self.table} WHERE epk_id={id}""")
                user_row = cursor.fetchone()

        User = UserGateway()
        User.epk_id = user_row[0]
        User.login = user_row[1]
        User.password = user_row[2]
        return User


class UserGateway:
    def __init__(self):
        self.epk_id = None
        self.login = None
        self.password = None

        ##-- table
        self.table = 'Users'
        pass

    def Insert(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""INSERT INTO {self.table} (login, pass) 
                                    VALUES ({self.login}, '{self.password}')""")
                conn.commit()
        return

    def Update(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""UPDATE {self.table} SET login='{self.login}' 
                                    WHERE portfolio_id={self.epk_id}""")
                conn.commit()
        return

    def Delete(self):
        conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
        with closing(psycopg2.connect(conn_string)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"""DELETE FROM {self.table} WHERE portfolio_id={self.epk_id}""")
                conn.commit()
        return

