from django.shortcuts import redirect, render , get_object_or_404
from django.http import HttpResponse
from .models import Person,Catalog 

def index(request):
    catalog = Catalog.objects.order_by('-type_cat') 
    return render(request,"scammerlist/index.html",{'catalog':catalog}) 

def search(request):
    getname = request.GET['search_name']
    search_cat = request.GET['search_cat']
    if search_cat == 'all':
        results = Person.objects.filter(name__contains=getname) # Every person in all catalog
        resultsemail = Person.objects.filter(email__contains=getname)
    else:
        catalog = get_object_or_404(Catalog,pk=int(search_cat))
        results = catalog.person_set.filter(name__contains=getname) # Every person in all catalog
        resultsemail = catalog.person_set.filter(email__contains=getname)
        
    result_text = ""
    if len(results) == 0:
        result_text = "Not found"
        results = None
    else: # found
        result_text = "Found : " + str(len(results)) + " people"
        
            
    return render(request,"scammerlist/searchresults.html", {'results_text':result_text,
   'results':results ,'resultsemail':resultsemail}) 
    
def listname(request,catalog_id):
    catalog = get_object_or_404(Catalog,pk=catalog_id)
    return render(request,"scammerlist/detail.html",{"catalog":catalog})
    
def persondetail(request,person_id):
    person = get_object_or_404(Person,pk=person_id)
    return render(request,"scammerlist/detail_sub.html",{"person":person})
    
def addperson(request):
    catalog_all = Catalog.objects.order_by('-type_cat')
    if request.method == 'POST':
        catalog_id = int(request.POST['catalog']) # convert string ot int
        catalog = get_object_or_404(Catalog,pk=catalog_id)
        print(catalog_id)
        catalog.person_set.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile_number=request.POST['mobile'],
            detail=request.POST['detail'],
            )
        catalog.save()
        print("OK")
        return redirect('/') # redirect to homepage
    return render(request,"scammerlist/add.html",{"catalog_all":catalog_all})
