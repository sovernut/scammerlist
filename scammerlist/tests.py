from django.core.urlresolvers import resolve
from django.test import TestCase
from scammerlist.views import index
from scammerlist.models import Catalog,Person

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self): # enter url / its call function index
        found = resolve('/') 
        self.assertEqual(found.func, index) 
    
    def test_uses_home_template(self): # test that homepage use index.html
        response = self.client.get('/')
        self.assertTemplateUsed(response,'scammerlist/index.html')
