import sys
import traceback
from selenium.common.exceptions import NoSuchElementException

from database import Database
from csv_file import CsvFile
from web_data_tool.product_page import ProductPage, GetProductCodes
from web_data_tool.search_page import SearchPage


if __name__ == '__main__':

    demo_name = sys.argv[1] if len(sys.argv) > 1 else "demo1c"

    print(f'Initialising task - {demo_name}...')
    
    if demo_name == "demo1a":
        """ Demo 1a """
        src = CsvFile()
        print(""" ProductPage website get single product - write to """, src)        
        
        task1 = ProductPage(1, product_codes=["1403149"], base_url="https://www.argos.co.uk/product", datasource=src)
        print('Running task...')
        task1.run()
        
        print('Task closing...') 
        task1.close()


    if demo_name == "demo1b":
        """ Demo 1b """
        src = Database()
        print(" ProductPage - get single product - write to ", src)

        task1 = ProductPage(1, product_codes=["1403149"], base_url="https://www.argos.co.uk/product", datasource=src)
        
        print('Running task...')
        task1.run()
        
        print('Task closing...') 
        task1.close()


    if demo_name == "demo1c":
        """ Demo 1c """
        src = Database()
        print(" ProductPage - get all product codes for Mattress - write to ", src)

        task1 = GetProductCodes(1, search_terms="Matress", url="https://www.argos.co.uk/", datasource=src)
        
        print('Running task1 to get product code...')
        task1.run()

        # share src with task2
        task1.close(page_only=True)

        task2 = ProductPage(1, product_codes=task1.product_codes, base_url="https://www.argos.co.uk/product", datasource=src)
        print('Running task...')
        task2.run()
        
        print('Task closing...') 
        task2.close()


    elif demo_name == "demo2":
        """ Demo 2 """
        src = Database()
        print(" ProductPage - Search for matresses of different sizes on Argos website - write to ", src)

        matress_sizes = ["single"] #, "small-double", "double", "king-size"]
        
        for size in matress_sizes:
            task = SearchPage(1, search_terms="Matress", category=size, url=f"https://www.argos.co.uk/browse/home-and-furniture/bedroom-furniture/mattresses/c:29870/size:{size}", datasource=src)
            
            print('Running task...')
            task.run()
            
            print('Task closing...') 
            task.close()
            
            print('Task closed!!!')


    elif demo_name == "demo3":
        """ Demo 3 """
        src = Database()
        print(" ProductPage - Get matresses availablity - write to ", src)

        # Single mattresses page 3

        task = SearchPage(1, search_terms="Matress", category="single", postcode="HD4 6XX", url=f"https://www.argos.co.uk/browse/home-and-furniture/bedroom-furniture/mattresses/c:29870/size:single/opt/page:3/", datasource=src)
        
        print('Running task...')
        task.run()
        
        print('Task closing...') 
        task.close()
        
        print('Task closed!!!')
    
    else:
        print("A demo of that name does not exist!!!!!")

    print('Completed!!!!!!!')
