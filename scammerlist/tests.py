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
        
    def test_create_and_display_catalog(self):
        Catalog.objects.create(type_cat='ขายอาหารเสริม')
        response = self.client.get('/')
        self.assertIn('ขายอาหารเสริม', response.content.decode())
        
    def test_only_saves_when_necessary(self):
        self.client.get('/add_p') # go to addp
        self.assertEqual(Person.objects.count(), 0)
        
    def test_addp_was_real(self):
        response = self.client.get('/add_p')
        self.assertIn('Mobile Number', response.content.decode())
        
    def test_redirects_after_POST(self):
        response = self.client.post('/add_p/', 
                data={'catalog': '1',
                'name': 'Osas',
                'email': 'osasis@email.com',
                'mobile': '0854652228',
                'detail': 'scammer'})
                
        self.assertEqual(response.status_code, 302) # redirect code
        self.assertEqual(response['location'], '/') # redirect to home page '/'
        
