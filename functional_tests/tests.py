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
   



