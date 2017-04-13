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

    def test_title(self):
        self.browser.get('http://localhost:8000') # open app
        self.assertIn('scammer', self.browser.title)
        
        searchbox = self.browser.find_element_by_id('searchBox')
        self.assertEqual(
            searchbox.get_attribute('placeholder'),
            'Enter name'
        )
        searchbox.send_keys('X')
        searchbox.send_keys(Keys.ENTER)
        time.sleep(2)
        table = self.browser.find_element_by_id('result_table')
        rows = table.find_elements_by_tag_name('td')
        self.assertIn('X (ขายเกม)', [row.text for row in rows])
        
        
        self.fail('Finish the test!')



