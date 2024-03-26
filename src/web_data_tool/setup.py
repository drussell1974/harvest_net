import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r"../sqlite/test.db"

    sql_create_run_table = """CREATE TABLE IF NOT EXISTS run (
                                    id integer PRIMARY KEY,
                                    begin_date text NOT NULL,
                                    status_id integer NOT NULL
                                );"""


    sql_create_customer_table = """CREATE TABLE IF NOT EXISTS customer (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    url_path text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL
                                );"""


    sql_create_web_scraping_table = """ CREATE TABLE IF NOT EXISTS web_scraping (
                                        id integer PRIMARY KEY,
                                        run_id text NOT NULL references run (id),
                                        customer_id integer NOT NULL REFERENCES customer (id), 
                                        product_code text NOT NULL,
                                        lead_date text NULL,
                                        lead_days integer NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        print("Creating customer table...")
        create_table(conn, sql_create_customer_table)

        print("Creating run table...")
        create_table(conn, sql_create_run_table)

        print("Creating web_scraping table...")
        create_table(conn, sql_create_web_scraping_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()