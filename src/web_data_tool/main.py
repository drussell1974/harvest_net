import sys
import traceback
from selenium.common.exceptions import NoSuchElementException

from database import main as db_main
from demo1 import Demo1
from demo2 import Demo2

def setup():
    db_main()


if __name__ == '__main__':
    demo_name = sys.argv[1]
    print(f'Initialising task - {demo_name}...')

    if demo_name == "demo1":
        """ Demo 1 """
        """ Ad-hoc search on Argos website """

        task = Demo1(1, search_terms="Matress", url="https://www.argos.co.uk/")
        print('Running task...')
        task.run()
        
        print('Task closing...') 
        task.close()



    elif demo_name == "demo2":
        """ Demo 2 """
        """ Search for matresses of different sizes on Argos website """

        matress_sizes = ["single", "small-double", "double", "king-size"]
        
        for size in matress_sizes:
            task = Demo2(1, search_terms="Matress", category=size, url=f"https://www.argos.co.uk/browse/home-and-furniture/bedroom-furniture/mattresses/c:29870/size:{size}")
            
            print('Running task...')
            task.run()
            
            print('Task closing...') 
            task.close()
            
            print('Task closed!!!')



    print('Completed!!!!!!!')
