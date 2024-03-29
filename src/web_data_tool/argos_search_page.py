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


class ArgosSearchPage(Base):
    """ Task class for the demo run """

    TEST_URL = "http://www.google.com"
    
    def __init__(self, customer_id, search_terms, category, postcode=None, datasource=None, url=None):  
        super().__init__(datasource, url)
        
        # run
        self.customer_id = customer_id
        self.search_terms = search_terms
        self.postcode = postcode
        self.category = category
        self.run_id = 0
        self.begin_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.status_id = 0  # 0 = not started, 1 = running, 2 = completed, 3 = failed
        
        
    def run(self):
        """ Run the task """

        self.run_id = self.db.insert_run(self.customer_id, self.search_terms, self.category, self.begin_date, 1)
        
        self.do_get_page(self.url)
        
        # accept cookies - if present
        elem = self.find_element_with_explicit_wait(By.CSS_SELECTOR, "#explicit-consent-prompt-accept")
        if elem is not None:
            elem.click()

        # enter postcode
        if self.postcode is not None:
            elem = self.find_element_with_explicit_wait(By.CSS_SELECTOR, "button.Buttonstyles__Button-sc-42scm2-2:nth-child(2)")        
            elem.click()

            elem = self.find_element_with_explicit_wait(By.CSS_SELECTOR, "#postcode")
            elem.send_keys(self.postcode)
            elem.send_keys(Keys.RETURN)

        # get products

        elems = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id=".jsHfZV", wait=10)

        next_page = True

        while next_page is True:
            for elem in elems:
                try:
                    """ Find on index """

                    # product id from url - .../product/2650049?clickPR=plp:1:131
                    pc_elem = self.find_element_with_implicit_wait(By.CSS_SELECTOR, element_id='.cnmosm:first-child', parent=elem)
                    pc_text = pc_elem.get_attribute("href") if pc_elem is not None else 'NF'
                    
                    av_text = 'INIT'
                    if pc_text != 'NF':
                        pc_text = pc_text.split("?")[0] if len(pc_text.split("?")) > 0 else 'NF'
                        pc_text = pc_text.split('/')[len(pc_text.split("/"))-1] if pc_text != 'NF' and len(pc_text.split('/')) > 0 else 'NF'

                        # > .cnmosm div.ProductCardstyles__AvailabilityLabelContainer-h52kot-22.hMTBBA div.ProductCardstyles__AvailabilityLabelWrapper-h52kot-24.lgWlfG span.ProductCardstyles__AvailabilityLabel-h52kot-25.xrvSx
                        av_elem = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id='div.hMTBBA div.lgWlfG span.xrvSx', parent=pc_elem)    
                        av_text = av_elem.text if av_elem is not None else 'NF'
                        if av_text != 'NF':
                            print(av_text)
                    else: 'NF'

                    pn_elem = self.find_element_with_implicit_wait(By.CSS_SELECTOR, element_id='.PQnCV', parent=elem)
                    pn_text = pn_elem.text if pn_elem is not None else 'NF'

                    pr_elem = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id='.ProductCardstyles__PriceText-h52kot-16', parent=elem)
                    pr_text = pr_elem.text if pr_elem is not None else 'NF'

                    di_elem = self.find_element_with_implicit_wait(by=By.CSS_SELECTOR, element_id='.uhWEw', parent=elem)
                    di_text = di_elem.text if di_elem is not None else 'NF'

                    self.db.insert_data(self.run_id, pc_text, pn_text, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), 0, av_text, pr_text, di_text)

                except Exception as e:
                    print(e)
            

            # commit current results
                    
            #self.db.conn.commit()
            
            # pagination - go to next page
            elem = self.find_element_with_implicit_wait(By.CSS_SELECTOR, 'a.Paginationstyles__PageLink-sc-1temk9l-1')
            try:
                print("opening next page....")
                elem.click()
            except StaleElementReferenceException  as e:
                elem = self.find_element_with_implicit_wait(By.CSS_SELECTOR, 'a.Paginationstyles__PageLink-sc-1temk9l-1')
                elem.click()  
            except Exception as e:    
                next_page = False
            
            if elem is not None:        
                next_page = True


        pass


    def close(self):
        super().close()
