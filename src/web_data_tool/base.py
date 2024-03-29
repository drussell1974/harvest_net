import time
from datetime import datetime
from unittest import TestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

from database import Database

def WebBrowserContext():

    ''' Uncomment Chrome driver -- chromedriver.exe '''
    #options = webdriver.ChromeOptions()
    #options.add_argument("--start-maximized")
    #return webdriver.Chrome()
    
    ''' Uncomment for Firefox -- geckodriver.exe '''
    #fireFoxOptions = webdriver.FirefoxOptions()
    #fireFoxOptions.add_argument("--headless")
    #fireFoxOptions.set_headless()
    #browser = webdriver.Firefox(options=fireFoxOptions)
    
    #return browser

    driver = webdriver.Firefox()
    return driver


class Base(TestCase):

    url = None

    def __init__(self, url):                                                                
        super().__init__()

        self.db = Database()
        
        self.url = url if url is not None and url != "" else self.TEST_URL                                                                    

        self.test_context = WebBrowserContext()
        self.test_context.implicitly_wait(3)
        self.test_context.maximize_window()
        self.test_context.set_page_load_timeout(30)
        self.test_context.set_script_timeout(30)
        self.test_context.delete_all_cookies()
        

    def wait(self, s = 3):
        time.sleep(s)


    def do_get_page(self, uri, wait=0):
        """ open the web page"""
        self.test_context.get(uri)
        self.test_context.implicitly_wait(wait)


    def find_elements_with_implicit_wait(self, by, element_id, wait=2):
        self.test_context.implicitly_wait(wait)
        elem = self.test_context.find_elements(by=by, value=element_id)
        return elem


    def find_elements_with_explicit_wait(self, by, element_id, wait=2):
        elem = WebDriverWait(self.test_context, wait).until(
            EC.presence_of_all_elements_located((by, element_id))
        )
        return elem


    def find_element_with_implicit_wait(self, by, element_id, wait=2, parent=None):
        self.test_context.implicitly_wait(wait)
        elem = None
        try:
            if parent == None:
                elem = self.test_context.find_element(by=by, value=element_id)
            else:
                elem = parent.find_element(by=by, value=element_id)
        except NoSuchElementException:
            print(f"Element '{element_id}' not found")
        return elem


    def find_element_with_explicit_wait(self, by, element_id, wait=2, parent=None):
        elem = None
        try:
            elem = self.test_context if parent == None else parent
            elem = WebDriverWait(elem, wait).until(
                EC.presence_of_element_located((by, element_id))
            )
        except TimeoutException:
            print(f"Timeout out waiting for element '{element_id}' to load")
        except NoSuchElementException:
            print(f"Element '{element_id}' not found")
        return elem


    def click_element(self, by, value):
        elem = self.test_context.find_element(by, value)
        elem.click()


    def close(self):
        self.test_context.quit()
        self.test_context = None

        self.db.conn.commit()