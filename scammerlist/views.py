from django.shortcuts import render 
from django.http import HttpResponse
from .models import Person,Catalog 

def index(request):
    catalog = Catalog.objects.order_by('-type_cat') 
    return render(request,"scammerlist/index.html",{'catalog':catalog}) 

def search(request):
    query = request.GET['search_name']
    print(query)
    return index(request)
