from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import Person,Catalog 

def index(request):
    catalog = Catalog.objects.order_by('-type_cat') 
    return render(request,"scammerlist/index.html",{'catalog':catalog}) 

def search(request):
    getname = request.GET['search_name']
    results = Person.objects.filter(name=getname) # Every person in all catalog
    result_text = ""
    if len(results) == 0:
        result_text = "Not found"
        results = None
    else: # found
        result_text = "Found : " + str(len(results)) + " people"
        
            
    return render(request,"scammerlist/searchresults.html",     {'results_text':result_text,
   'results':results }) 
    
def listname(request,catalog_id):
    catalog = get_object_or_404(Catalog,pk=catalog_id)
    return render(request,"scammerlist/detail.html",{"catalog":catalog})
    
def persondetail(request,person_id):
    person = get_object_or_404(Person,pk=person_id)
    return render(request,"scammerlist/detail_sub.html",{"person":person})
