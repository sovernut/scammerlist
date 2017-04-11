from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:8000/scammer') # open app

        self.assertIn('scammer', self.browser.title)

        self.fail('Finish the test!')




if __name__ == '__main__':
    unittest.main()

