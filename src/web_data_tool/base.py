import time
from unittest import TestCase
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
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

    service = Service(service_args=['--profile-root', './firefox_profile'])
    
    firefox_profile = FirefoxProfile()
    
    """firefox_profile.set_preference("javascript.enabled", True)
    firefox_profile.set_preference("network.cookie.cookieBehavior", 0)
    firefox_profile.set_preference("network.cookie.lifetimePolicy", 2)
    firefox_profile.set_preference("network.cookie.thirdparty.sessionOnly", False)
    firefox_profile.set_preference("network.cookie.thirdparty.nonsecureSessionOnly", True)"""
    
    firefox_profile.set_preference("pref.privacy.disable_button.tracking_protection_exceptions", True)
    firefox_profile.set_preference("privacy.trackingprotection.enabled", False)
    
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.profile = firefox_profile

    browser = webdriver.Firefox(options=fireFoxOptions, service=service)
    return browser
    

class Base(TestCase):

    url = None

    def __init__(self, url, datasource=None, DEBUG=False, **kwargs):                                                                
        super().__init__()
        
        self.DEBUG = DEBUG
        
        self.db = datasource if datasource is not None else Database()
        
        self.url = url if url is not None and url != "" else self.TEST_URL                                                                    
        
        self.test_context = None
        self.get_connection()


    def get_connection(self):
        if self.test_context is None:
            self.test_context = WebBrowserContext()
            self.test_context.implicitly_wait(3)
            self.test_context.maximize_window()
            self.test_context.set_page_load_timeout(30)
            self.test_context.set_script_timeout(30)
            #self.test_context.delete_all_cookies()
        return self.test_context
        

    def wait(self, s = 3):
        time.sleep(s)


    def do_get_page(self, uri, wait=0):
        """ open the web page"""
        self.get_connection()
        self.test_context.get(uri)
        self.test_context.implicitly_wait(wait)


    def find_elements_with_implicit_wait(self, by, element_id, wait=2, max_depth=3):
        elem = None

        try:
            self.test_context.implicitly_wait(wait)
            elem = self.test_context.find_elements(by=by, value=element_id)
        
        except StaleElementReferenceException as sere:
            print(f"Element '{element_id}' not found - {sere}. Trying again...")
            if max_depth > 0:
                elem = self.find_elements_with_implicit_wait(by, element_id, wait=2, max_depth=max_depth-1)
        except TimeoutException as toe:
            print(f"Timeout out waiting for element '{element_id}' to load - {toe}")
        except NoSuchElementException as nsee:
            print(f"Element '{element_id}' not found - {nsee}")

        return elem


    def find_elements_with_explicit_wait(self, by, element_id, wait=2, max_depth=3):
        elem = None
        
        try:
            elem = WebDriverWait(self.test_context, wait).until(
                EC.presence_of_all_elements_located((by, element_id))
            )
        
        except StaleElementReferenceException as sere:
            print(f"Element '{element_id}' not found - {sere}")
            if max_depth > 0:
                elem = self.find_elements_with_implicit_wait(by, element_id, wait=2, max_depth=max_depth - 1)
        except TimeoutException as toe:
            print(f"Timeout out waiting for element '{element_id}' to load - {toe}")
        except NoSuchElementException as nsee:
            print(f"Element '{element_id}' not found - {nsee}")

        return elem


    def find_element_with_implicit_wait(self, by, element_id, wait=2, parent=None, max_depth=3):
        elem = None
        
        self.test_context.implicitly_wait(wait)
        try:
            if parent == None:
                elem = self.test_context.find_element(by=by, value=element_id)
            else:
                elem = parent.find_element(by=by, value=element_id)
        
        except StaleElementReferenceException as sere:
            print(f"Element '{element_id}' not found - {sere}")
            if max_depth > 0:
                elem = self.find_elements_with_implicit_wait(by, element_id, wait=2, max_depth=max_depth - 1)
        except TimeoutException as toe:
            print(f"Timeout out waiting for element '{element_id}' to load - {toe}")
        except NoSuchElementException as nsee:
            print(f"Element '{element_id}' not found - {nsee}")

        return elem


    def find_element_with_explicit_wait(self, by, element_id, wait=2, parent=None, max_depth=3):
        elem = None

        try:
            elem = self.test_context if parent == None else parent
            elem = WebDriverWait(elem, wait).until(
                EC.presence_of_element_located((by, element_id))
            )
        except StaleElementReferenceException as sere:
            print(f"Element '{element_id}' not found - {sere}")
            if max_depth > 0:
                elem = self.find_elements_with_implicit_wait(by, element_id, wait=2, max_depth=max_depth - 1)
        except TimeoutException as toe:
            print(f"Timeout out waiting for element '{element_id}' to load - {toe}")
        except NoSuchElementException as nsee:
            print(f"Element '{element_id}' not found - {nsee}")

        return elem


    def click_element(self, by, value):
        elem = self.test_context.find_element(by, value)
        elem.click()


    def close(self, page_only=False):
        if self.db is not None and not page_only:
            """ close datasource """
            self.db.close()
        if self.test_context is not None:    
            """ close brower """
            self.test_context.quit()
            self.test_context = None
        