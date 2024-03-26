import time
from datetime import datetime
from unittest import TestCase

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


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

    def __init__(self, test):                                                                
        self.id = 0,
        self.begin_date = datetime.now(),
        self.status_id = 0  # 0 = not started, 1 = running, 2 = completed, 3 = failed

        super().__init__() 
        

    def wait(self, s = 3):
        time.sleep(s)


    def do_get(self, uri, wait=0):
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


    def find_element_with_implicit_wait(self, by, element_id, wait=2):
        self.test_context.implicitly_wait(wait)
        elem = self.test_context.find_element(by=by, value=element_id)
        return elem


    def find_element_with_explicit_wait(self, by, element_id, wait=2):
        elem = WebDriverWait(self.test_context, wait).until(
            EC.presence_of_element_located((by, element_id))
        )
        return elem


    def click_element(self, by, value):
        elem = self.test_context.find_element(by, value)
        elem.click()


    def close(self):
        """ Close the task """
        self.test_context.quit()
        self.test_context = None