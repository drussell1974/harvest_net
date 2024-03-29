import csv
import datetime

class CsvFile:

    def __init__(self):
        self.conn = self.create_connection()
        

    def insert_run(self, *vals):
        """ DO NOTHING """
        pass
    

    def insert_data(self, *vals):
        """ run_id, product_code, product_name, lead_date, lead_days, in_stock, price, discount """

        insert_data_txt = []
        insert_data_txt = insert_data_txt.append(vals)
        print("web_scraping...", vals)
        self.exec(self.conn, insert_data_txt)
        

    @classmethod
    def create_connection(cls):
        """ Create a connection to a csv file"""
        path = f"./test_{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.csv"
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        return writer
        

    @classmethod
    def exec(cls, writer, data):
        """ Write data to csv file """
        if writer is None:
            writer = cls.create_connection()
        writer.writerow(data)
