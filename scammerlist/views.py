from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import Person,Catalog 

def index(request):
    catalog = Catalog.objects.order_by('-type_cat') 
    return render(request,"scammerlist/index.html",{'catalog':catalog}) 

def search(request):
    query = request.GET['search_name']
    print(query)
    return index(request)
    
def listname(request,catalog_id):
    catalog = get_object_or_404(Catalog,pk=catalog_id)
    catalog = catalog.person_set.all()
    return render(request,"scammerlist/detail.html",{"catalog":catalog})
