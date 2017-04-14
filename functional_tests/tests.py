from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
import unittest
from scammerlist.models import Catalog , Person

class NewVisitorTest(unittest.TestCase): # test in existing database

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_title_and_search_box(self):
        self.browser.get('http://localhost:8000') # open app
        self.assertIn('Scammer', self.browser.title)
        
        searchbox = self.browser.find_element_by_id('searchBox')
        self.assertEqual(
            searchbox.get_attribute('placeholder'),
            'Enter name'
        )
        searchbox.send_keys('X')
        searchbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element_by_id('result_ul')
        rows = table.find_elements_by_tag_name('li')
        self.assertIn('X (ขายเกม)', [row.text for row in rows])
        
    
'''class NewVisitorModifyData(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()
        
    def test_user_add_person(self):
            self.browser.get(self.live_server_url+'/add_p') # open app add person
            self.findid_and_enterinput('catalog','0') # created_catalog
            self.findid_and_enterinput('name','Osas')
            self.findid_and_enterinput('email','abc@acgmail.com')
            self.findid_and_enterinput('mobile','0985462135')
            self.findid_and_enterinput('detail','sell')
            addbtn = self.browser.find_element_by_id('add_btn')
            addbtn.click()
            time.sleep(2)
            self.browser.get(self.live_server_url+'/list/0')
            table = self.browser.find_element_by_id('table_list')
            rows = table.find_elements_by_tag_name('tr')
            self.assertIn('Osas abc@acgmail.com sell', [row.text for row in rows])
        
    def findid_and_enterinput(self,id_in,text):
        thisbox = self.browser.find_element_by_id(id_in)
        thisbox.send_keys(text)'''

