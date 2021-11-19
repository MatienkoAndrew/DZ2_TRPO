import psycopg2
from contextlib import closing


def main():
    conn_string = "host='localhost' dbname='postgres' user='a19053183' password=''"
    # print the connection string we will use to connect
    # print("Connecting to database\n	->%s" % (conn_string))

    # get a connection, if a connect cannot be made an exception will be raised here
    with closing(psycopg2.connect(conn_string)) as conn:

        with conn.cursor() as cursor:
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            cursor = conn.cursor()

            cursor.execute("DELETE FROM Users WHERE login='Nastya'")
            # cursor.execute("INSERT INTO Users (login, pass) VALUES('Nastya', '1234')")

            ##-- При создании нового клиента - создается новый портфель
            cursor.execute("""
                        with new_order as (
                        insert into Users (login, pass) values ('Nastya', '1234')
                          returning epk_id
                        )
                        insert into Portfolios (epk_id, portfolio_name)
                        values
                        (
                          (select epk_id from new_order),
                          'test'
                        );
                        """)


            # cursor.execute("""UPDATE Users
            #                     SET login='Andrew'
            #                     WHERE login='Nastya'
            #                 """)

            # execute our Query
            cursor.execute("SELECT * FROM Users")

            # retrieve the records from the database
            records = cursor.fetchall()

            print(records)
            conn.commit()


if __name__ == "__main__":
    main()


# CREATE TABLE Users (
# epk_id SERIAL PRIMARY KEY,
# login TEXT,
# pass TEXT);


# CREATE TABLE Portfolios (
# id SERIAL PRIMARY KEY,
# epk_id INTEGER,
# portfolio_name TEXT,
# FOREIGN KEY (epk_id) REFERENCES Users(id)
# );


# CREATE TABLE Assets(
# assets_id SERIAL PRIMARY KEY,
# asset_name TEXT,
# price Decimal(12,2)
# );


# CREATE TABLE Portfolio_to_Assets (
# id SERIAL PRIMARY KEY,
# portfolio_id INTEGER, assets_id INTEGER,
# FOREIGN KEY(portfolio_id) REFERENCES Portfolios (id),
# FOREIGN KEY(assets_id) REFERENCES Assets (assets_id));
# );
