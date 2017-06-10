from django.shortcuts import redirect, render , get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Person,Catalog,Report
from django.contrib.auth.models import User

def login_request(request):
    # if there are username in textbox
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # found username then login
        if user is not None:
            login(request,user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
   
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
    
def registration(request):
    username = request.POST.get('username','Unknown')
    password = request.POST.get('password','Unknown')
    if 'username' in request.POST and 'password' in request.POST:
        new_user = User.objects.create_user(username=username,password=password)
        new_user.save()
    return render(request, 'scammerlist/registration_complete.html', {'username':username})
    
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
        results = catalog.person_set.filter(name__contains=getname) # Every person in filtered catalog
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
    
def persondetail(request,person_id,loginrequire=""):
    person = get_object_or_404(Person,pk=person_id)
    return render(request,"scammerlist/detail_sub.html",{"person":person,"loginrequire":loginrequire})
    
def personreport(request,person_id):
    if request.user.is_authenticated:
        person = get_object_or_404(Person,pk=person_id)
        return render(request,"scammerlist/report.html",{"person":person})
    else:
        loginrequire = "กรุณา login เพื่อทำการ report"
        return persondetail(request,person_id,loginrequire)

def save_reported(request,person_id):
    # for saveing report
    report_detail = request.POST['report']
    person = get_object_or_404(Person,pk=person_id)
    report_time = timezone.now()
    person.last_report_time = report_time
    person.save()
    person.report_set.create(report_detail=report_detail,report_time=report_time,
                             reporter_name=request.user)
    return HttpResponseRedirect(reverse('person_de',kwargs={'person_id':person_id}))
    
def show_reported(request):
    people = Person.objects.all()
    return render(request,"scammerlist/report_detail.html",{"people":people})

    
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
            picture_url=request.POST['picture'],
            )
        catalog.save()
        print("OK")
        return redirect('/') # redirect to homepage
    return render(request,"scammerlist/add.html",{"catalog_all":catalog_all})
    
def show_about(request):
    return render(request,"scammerlist/about.html")
