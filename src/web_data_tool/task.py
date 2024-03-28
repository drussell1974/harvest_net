import time
import os
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base import Base, WebBrowserContext


class Demo1(Base):
    """ Task class for the test run """

    TEST_URL = "http://www.google.com"
    
    def __init__(self, customer_id, test_page=None):  
        super().__init__(test_page)   
        
        # run
        self.customer_id = customer_id
        self.run_id = 0
        self.begin_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.status_id = 0  # 0 = not started, 1 = running, 2 = completed, 3 = failed
        
        
    def run(self):
        """ Run the task """

        self.run_id = self.db.insert_run(self.customer_id, self.begin_date, 1)
        
        self.do_get(self.test_page)
        
        # accept cookies
        elem = WebDriverWait(self.test_context, 2).until(
            EC.presence_of_element_located((By.ID, "explicit-consent-prompt-accept"))
        )
        elem.click()

        # enter search term
        elem = self.test_context.find_element(by=By.ID, value="searchTerm")
        
        elem.send_keys("Matress")
        
        elem = self.test_context.find_element(by=By.CSS_SELECTOR, value="._2mKaC")
        elem.click()

        WebDriverWait(self.test_context, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.M052styles__Link-sc-1cubg5c-7:nth-child(1) > picture:nth-child(1) > img:nth-child(3)"))
        ).click()
            
        # get products

        elems = self.test_context.find_elements(by=By.CSS_SELECTOR, value=".dedmXK")
        
        for elem in elems:
            try:
                """ Find on page"""
                pn = self.find_element_with_implicit_wait(By.CSS_SELECTOR, '.PQnCV', parent=elem)
                pn = pn.text if pn is not None else 'NF'

                pr = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id='.ProductCardstyles__PriceText-h52kot-16', parent=elem)
                pr = pr.text if pr is not None else 'NF'

                di = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id='.uhWEw', parent=elem)
                di = di.text if di is not None else 'NF'

                self.db.insert_data(self.run_id, '', pn, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 0, 0, pr, di)
            except Exception as e:
                print(e)
            
        pass



    def close(self):
        super().close()

