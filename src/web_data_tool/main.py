import traceback
from selenium.common.exceptions import NoSuchElementException

from database import main as db_main
from task import Demo1

def setup():
    db_main()


if __name__ == '__main__':

    print('Initialising task...')

    task = Demo1(1, "https://www.argos.co.uk/")
    
    print('Running task...')
    task.run()
    
    print('Task closing...') 
    task.close()

    print('Task closed!!!!!!!') 

