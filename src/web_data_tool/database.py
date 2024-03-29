import sqlite3
from sqlite3 import Error


class Database:

    def __init__(self):
        setup()
        self.conn = self.create_connection()
        

    def insert_run(self, *vals):
        """ INSERT run (customer_id, search_terms, category, begin_date, status_id) ..."""
        
        insert_run_sql = f"INSERT INTO run (customer_id, search_terms, category, begin_date, status_id) VALUES {vals};"
        print("run...", insert_run_sql)
        self.exec(self.conn, insert_run_sql)
        return self.get_last_insert_rowid(self.conn)
    

    def insert_data(self, *vals):
        """INSERT web_scraping (run_id, order_of_result, product_id, product_code, product_name, lead_date, lead_days, in_stock, price, discount) ..."""
        
        insert_data_sql = f"INSERT INTO web_scraping (run_id, order_of_result, product_id, product_code, product_name, lead_date, lead_days, in_stock, price, discount) VALUES {vals};"
        print("web_scraping...", vals)
        self.exec(self.conn, insert_data_sql)
        return self.get_last_insert_rowid(self.conn)
        

    @classmethod
    def create_connection(cls):
        conn = sqlite3.connect("./test.db")
        return conn
        
    @classmethod
    def exec(cls, conn, sql_stmt):
        c = conn.cursor()
        r = c.execute(sql_stmt)
        return r


    @classmethod
    def create_table(cls, conn, sql_stmt):
        cls.exec(conn, sql_stmt)


    @classmethod
    def get_last_insert_rowid(self, conn):
        result = self.exec(conn, "SELECT last_insert_rowid();").fetchone()[0]
        print("Result:", result)
        return result

    def close(self):
        self.conn.commit()


def setup():
    


    sql_create_customer_table = """CREATE TABLE IF NOT EXISTS customer (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    url_path text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL
                                );"""

    sql_create_run_table = """CREATE TABLE IF NOT EXISTS run (
                                    id integer PRIMARY KEY,
                                    customer_id integer NOT NULL REFERENCES customer (id), 
                                    search_terms text NOT NULL,
                                    category text NOT NULL,
                                    begin_date text NOT NULL,
                                    status_id integer NOT NULL
                                );"""

    sql_create_web_scraping_table = """ CREATE TABLE IF NOT EXISTS web_scraping (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        run_id text NOT NULL references run (id),
                                        order_of_result integer NOT NULL,
                                        product_id integer NULL,
                                        product_code text NULL,
                                        product_name text NULL,
                                        lead_date text NULL,
                                        lead_days integer NULL,
                                        in_stock integer NOT NULL DEFAULT 0,
                                        price real NULL,
                                        discount real NULL
                                    ); """
    
    sql_alter_web_scraping_table = """ ALTER TABLE web_scraping
                                        ADD COLUMN product_id integer AFTER run_id;
                                    """

    # create a database connection
    conn = Database.create_connection()

    # create tables
    if conn is not None:
        print("Creating customer table...")
        Database.exec(conn, sql_create_customer_table)

        print("Creating run table...")
        Database.exec(conn, sql_create_run_table)

        print("Creating web_scraping table...")
        Database.exec(conn, sql_create_web_scraping_table)

        #print("Altering web_scraping table...")
        #Database.create_table(conn, sql_alter_web_scraping_table)
    else:
        print("Error! cannot create the database connection.")
    
    conn.close()


if __name__ == '__main__':
    print("Setting up Database...")
    
    setup()
    
    print("Database setup complete.")