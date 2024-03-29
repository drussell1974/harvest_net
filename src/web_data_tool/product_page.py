import time
import os
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base import Base, WebBrowserContext


class ProductPage(Base):
    """ Task class for the demo run """
    
    def __init__(self, customer_id, product_codes, category="ad-hoc", base_url=None, datasource=None):  
        super().__init__(base_url, datasource)
        
        # run
        self.customer_id = customer_id
        self.product_codes = product_codes
        self.category = category
        self.run_id = 0
        self.begin_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.status_id = 0  # 0 = not started, 1 = running, 2 = completed, 3 = failed
        

    def run(self):
        """ Run the task """

        self.run_id = self.db.insert_run(self.customer_id, str(self.product_codes), self.category, self.begin_date, 1)
        print("creating run....", self.run_id)

        for product_code in self.product_codes:

            self.do_get_page(f"{self.url}/{product_code}")
                
            # accept cookies
            elem = self.find_element_with_explicit_wait(By.ID, "explicit-consent-prompt-accept")
            if elem is not None:
                elem.click()
            
            """ Find on page"""
            
            pc_elem = self.find_element_with_explicit_wait(By.CSS_SELECTOR, '.Namestyles__Main-sc-269llv-1 > span:nth-child(1)')
            pc_text = pc_elem.text if pc_elem is not None else 'NF'

            pn_elem = self.find_element_with_explicit_wait(By.CSS_SELECTOR, '.Namestyles__CatNumber-sc-269llv-2')
            pn_text = pn_elem.text if pn_elem is not None else 'NF'

            pr_elem = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id='.Pricestyles__OfferPriceTitle-sc-1oev7i-4')
            pr_text = pr_elem.text if pr_elem is not None else 'NF'

            di_elem = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id='.Pricestyles__PriceWas-sc-1oev7i-3')
            di_text = di_elem.text if di_elem is not None else 'NF'
            # run_id, product_code, product_name, lead_date, lead_days, in_stock, price, discount
            self.db.insert_data(self.run_id, product_code, pc_text, pn_text, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 0, 0, pr_text, di_text)
            
            self.close(page_only=True)
    

    def close(self, page_only=False):
        return super().close(page_only)
        

class GetProductCodes(Base):
    """ Task class for the demo run """
    
    def __init__(self, customer_id, search_terms, category="ad-hoc", datasource=None, url=None):  
        super().__init__(url, datasource)   
        
        # run
        self.customer_id = customer_id
        self.search_terms = search_terms
        self.category = category
        self.run_id = 0
        self.begin_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.status_id = 0  # 0 = not started, 1 = running, 2 = completed, 3 = failed
        
        
    def run(self):
        """ Run the task """

        self.do_get_page(self.url)
        
        # accept cookies
        elem = self.find_element_with_explicit_wait(By.ID, "explicit-consent-prompt-accept")
        if elem is not None:
            elem.click()

        # enter search term
        elem = self.test_context.find_element(by=By.ID, value="searchTerm")
        
        elem.send_keys(self.search_terms)
        
        elem = self.test_context.find_element(by=By.CSS_SELECTOR, value="._2mKaC")
        elem.click()

        WebDriverWait(self.test_context, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.M052styles__Link-sc-1cubg5c-7:nth-child(1) > picture:nth-child(1) > img:nth-child(3)"))
        ).click()
            
        # get products

        elems = self.test_context.find_elements(by=By.CSS_SELECTOR, value=".dedmXK")
        self.product_codes = []
        
        next_page = True
        n = 0
        while next_page is True:
            # get product codes from page
            for elem in elems:
                n = n + 1
                try:
                    # product id from url - .../product/2650049?clickPR=plp:1:131
                    pc = self.find_element_with_implicit_wait(By.CSS_SELECTOR, element_id='.cnmosm:first-child', parent=elem)
                    pc = pc.get_attribute("href") if pc is not None else 'NF'
                    if pc != 'NF':
                        pc = pc.split("?")[0] if len(pc.split("?")) > 0 else 'NF'
                        pc = pc.split('/')[len(pc.split("/"))-1] if pc != 'NF' and len(pc.split('/')) > 0 else 'NF'
                        print(pc)
                    else: 'NF'
                    
                    if pc != 'NF':
                        self.product_codes.append(pc)
                except Exception as e:
                    # just report and continue
                    print("Product code not found - ", e)
            
            # pagination - go to next page
            elem = self.find_element_with_implicit_wait(By.CSS_SELECTOR, 'a.Paginationstyles__PageLink-sc-1temk9l-1:last-child')
            if elem is not None:
                elem.click()
            else:
                next_page = False
        
            # commit current results
            
            # pagination - go to next page
            elem = self.find_element_with_implicit_wait(By.CSS_SELECTOR, 'a.Paginationstyles__PageLink-sc-1temk9l-1')
            try:
                print("opening next page....")
                elem.click()
            except StaleElementReferenceException  as e:
                elem = self.find_element_with_implicit_wait(By.CSS_SELECTOR, 'a.Paginationstyles__PageLink-sc-1temk9l-1')
                elem.click()  
            except Exception as e:
                elem = None    
                next_page = False
            
            if elem is None or n > 300:
                next_page = False
            else: 
                next_page = True
        
        return self.product_codes
    

    def close(self, page_only=False):
        return super().close(page_only)
        
    