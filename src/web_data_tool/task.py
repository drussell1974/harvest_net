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


"""Find Element By ID"""
# > elem = self.test_context.find_element(by=By.ID, value=element_id)

"""Find Element By CSS Selector"""
# > elem = self.test_context.find_element(by=By.CSS_SELECTOR, value=element_css_selector)
# > elems = self.test_context.find_elements(by=By.CSS_SELECTOR, value=element_css_selector)

"""Find Element By Class Name""" 
# > elem = self.test_context.find_element(by=By.CLASS_NAME, value=element_class_name)
# > elems = self.test_context.find_elements(By.CLASS_NAME, value=element_class_name)

"""Find Element By Tag Name"""
# > elem = self.test_context.find_element(by=By.TAG_NAME, value=element_tag_name)
# > elems = self.test_context.find_elements(By.TAG_NAME, value=element_tag_name)

"""Find Element By Name"""
# > elem = self.test_context.find_element(by=By.NAME, value=element_name)
# > elems = self.test_context.find_elements(By.NAME, value=element_name)

"""Find Element By Link Text"""
# > elem = self.test_context.find_element(by=By.LINK_TEXT, value=element_link_text)
# > elems = self.test_context.find_elements(By.LINK_TEXT, value=element_link_text)

"""Find Element By Partial Link Text"""
# > elem = self.test_context.find_element(by=By.PARTIAL_LINK_TEXT, value=element_partial_link_text)
# > elems = self.test_context.find_elements(By.PARTIAL_LINK_TEXT, value=element_partial_link_text)

"""Find Element By XPath""" 
# > elem = self.test_context.find_element(by=By.XPATH, value=element_xpath)
# > elems = self.test_context.find_elements(By.XPATH, value=element_xpath)


"""Enter values for input fields"""

# > self.test_context.find_element_by_id("search").send_keys("Something to find")
# > self.test_context.find_elements(By.ID, "search").send_keys("Something to find")

"""Click Element"""
# > self.test_context.find_element(by=By.XPATH, "//div[3]").click()

class Task(Base):
    """ Task class for the test run """
    TEST_URL = "http://www.google.com"

    def __init__(self, test_page=None):    
        
        test_page if test_page is not None and test_page != "" else self.TEST_URL                                                            
        
        super().__init__(test_page) 
        
        self.test_context = WebBrowserContext()
        self.test_context.implicitly_wait(3)
        self.test_context.maximize_window()
        self.test_context.set_page_load_timeout(30)
        self.test_context.set_script_timeout(30)
        self.test_context.delete_all_cookies()
        
        self.do_get(self.test_page)
        
        
    def run(self):
        """ Run the task """
        self.test_context.find_element(by=By.ID, value="search").send_keys("Something to find")
        pass


    def close(self):
        super().close()
