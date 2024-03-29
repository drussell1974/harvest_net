import sys
import traceback
from selenium.common.exceptions import NoSuchElementException

from database import Database
from csv_file import CsvFile
from argos_product_page import ArgosProductPage, GetProductCodes
from argos_search_page import ArgosSearchPage

def setup():
    db_main()


if __name__ == '__main__':
    demo_name = sys.argv[1]
    print(f'Initialising task - {demo_name}...')

    if demo_name == "demo1":
        """ Demo 1 """
        """ Ad-hoc search on Argos website """
        task1 = GetProductCodes(1, search_terms="Matress", datasource=Database(), url="https://www.argos.co.uk/")
        print('Running task1 to get product code...')
        task1.run()
        print('Task1 closing...') 
        task1.close()

        task2 = ArgosProductPage(1, product_codes=task1.product_codes, datasource=Database(), base_url="https://www.argos.co.uk/product")
        print('Running task...')
        task2.run()
        
        print('Task closing...') 
        task2.close()


    elif demo_name == "demo2":
        """ Demo 2 """
        """ Search for matresses of different sizes on Argos website """

        matress_sizes = ["single"] #, "small-double", "double", "king-size"]
        
        for size in matress_sizes:
            task = ArgosSearchPage(1, search_terms="Matress", category=size, datasource=Database(), url=f"https://www.argos.co.uk/browse/home-and-furniture/bedroom-furniture/mattresses/c:29870/size:{size}")
            
            print('Running task...')
            task.run()
            
            print('Task closing...') 
            task.close()
            
            print('Task closed!!!')


    elif demo_name == "demo3":
        """ Demo 3 """
        """ Get matress' availablity """
        
        # Single mattresses page 3

        task = ArgosSearchPage(1, search_terms="Matress", postcode="HD4 6XX", datasource=Database(), url=f"https://www.argos.co.uk/browse/home-and-furniture/bedroom-furniture/mattresses/c:29870/size:single/opt/page:3/")
        
        print('Running task...')
        task.run()
        
        print('Task closing...') 
        task.close()
        
        print('Task closed!!!')
        
    print('Completed!!!!!!!')
