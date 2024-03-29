import csv
import datetime

class CsvFile:

    def __init__(self):
        self._run_id = datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        self.conn = self.create_connection(self._run_id)
        self.insert_run("id", "run_id", "order_of_result", "product_id", "product_code", "product_name", "lead_date", "lead_days", "in_stock", "price", "discount")
        

    def insert_run(self, *vals):
        """ DO NOTHING """
        self.exec(self.conn, vals)
        return self.conn
    

    def insert_data(self, *vals):
        """ run_id, order_of_result, product_id, product_code, product_name, lead_date, lead_days, in_stock, price, discount """
        print("web_scraping...", vals)
        self.exec(self.conn, vals)
        

    def create_connection(self, run_id):
        """ Create a connection to a csv file"""
        path = f"./csv_files/test_{run_id}.csv"
        return open(path, 'w', newline='')
        
    
    @classmethod
    def exec(cls, *vals):
        """ Write data to csv file """
        w = csv.writer(vals[0], delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        w.writerow(list(vals[1])[1:])
    

    def close(self):
        self.conn.close()
