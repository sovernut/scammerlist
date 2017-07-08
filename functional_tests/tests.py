from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time
from scammerlist.models import Catalog , Person

class NewVisitorModifyData(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        c = Catalog(type_cat="ขายเกม")
        c.save()
        c.person_set.create(name="X",
            email="x@gmail.com",
            mobile_number="0876543215",
            detail="scammer")

    def tearDown(self):
        self.browser.quit()
        
    
    def test_title_and_search_box(self):
        # Bob want to search for scammer to decide whether to buy from X or not.
        # Bob found website name 'Scammer List' , he's enter.
        self.browser.get('http://localhost:8000') # open app
        self.assertIn('Scammer', self.browser.title)
        
        # He found searchbox which it's placeholder was "Enter name or email"
        searchbox = self.browser.find_element_by_id('searchBox')
        self.assertEqual(
            searchbox.get_attribute('placeholder'),
            'Enter name or email'
        )
        
        # He type 'X' and press enter
        searchbox.send_keys('X')
        searchbox.send_keys(Keys.ENTER)
        time.sleep(1)
        table = self.browser.find_element_by_id('result_ul')
        rows = table.find_elements_by_tag_name('li')
        
        # He found 'X' in list , so he's not buy from X.
        self.assertIn('X (ขายเกม)', [row.text for row in rows])
        
    def test_user_add_person(self):
        # Bob has been scam by Osas
        # He go to add scammer page
        self.browser.get(self.live_server_url+'/add_p') # open app add person
        
        # He types Osas's detail and click submit button
        self.findid_and_enterinput('catalog','0')
        self.findid_and_enterinput('name','Osas')
        self.findid_and_enterinput('email','abc@acgmail.com')
        self.findid_and_enterinput('mobile','0985462135')
        self.findid_and_enterinput('detail','sell')
        addbtn = self.browser.find_element_by_id('add_btn')
        addbtn.click()
        
        # He goes to Osas's page to see if it has been added.
        self.browser.get(self.live_server_url+'/list/2')
        time.sleep(1)
        table = self.browser.find_element_by_id('table_list')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('Osas abc@acgmail.com sell', [row.text for row in rows])
        
    def findid_and_enterinput(self,id_in,text):
        thisbox = self.browser.find_element_by_id(id_in)
        thisbox.send_keys(text)

