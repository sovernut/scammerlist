from django.shortcuts import redirect, render , get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Person,Catalog,Report
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

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
    theme = request.session.get('theme',"css/bootstrap.min.css")
    username = request.POST.get('username','Unknown')
    password = request.POST.get('password','Unknown')
    password1 = request.POST.get('conpassword','Unknown')
    regis = "Registration incomplete : can not get username or password"
    if 'username' in request.POST and 'password' in request.POST:
        if password != "" and username != "":
            if password == password1:
                if len(password) >= 8:
                    new_user = User.objects.create_user(username=username,password=password)
                    new_user.save()
                    regis = "Registration complete !"
                else:
                    regis = "Your password length must be 8 or more."
            else:
                regis = "Registration incomplete : your password doesn't match."
        else:
            regis = "Registration incomplete : You've leave a blank username/password."
    return render(request, 'scammerlist/registration_complete.html', {'username':username,
                                                                      'regis_status':regis,'theme':theme})
    

def change_password(request):
    theme = request.session.get('theme',"css/bootstrap.min.css")
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return render(request, 'scammerlist/registration_complete.html', 
                        {'username':request.user,'regis_status':'Change password successfully','theme':theme})
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'scammerlist/change_password.html', {
        'form': form, 'theme':theme })

def change_theme(request):
    theme = request.GET['theme']
    if theme == "black":
        request.session['theme'] = "css/bootstrap.min.flatdark.css"
    elif theme == "white":
        request.session['theme'] = "css/bootstrap.min.css"
    elif theme == "untitle":
        request.session['theme'] = "css/bootstrap.min.untitle.css"
    return HttpResponseRedirect(reverse('index'))
    
def index(request):
    theme = request.session.get('theme',"css/bootstrap.min.css")
    catalog = Catalog.objects.order_by('-type_cat') 
    return render(request,"scammerlist/index.html",{'catalog':catalog,
                                                    'theme':theme}) 

def search(request):
    theme = request.session.get('theme',"css/bootstrap.min.css")
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
   'results':results ,'resultsemail':resultsemail, 'theme':theme}) 
    
def listname(request,catalog_id):
    theme = request.session.get('theme',"css/bootstrap.min.css")
    catalog = get_object_or_404(Catalog,pk=catalog_id)
    return render(request,"scammerlist/detail.html",{"catalog":catalog, 'theme':theme})
    
def persondetail(request,person_id,loginrequire=""):
    theme = request.session.get('theme',"css/bootstrap.min.css")
    person = get_object_or_404(Person,pk=person_id)
    return render(request,"scammerlist/detail_sub.html",{"person":person, 
                                                        "loginrequire":loginrequire,
                                                        'theme':theme})
    
def personreport(request,person_id):
    theme = request.session.get('theme',"css/bootstrap.min.css")
    if request.user.is_authenticated:
        person = get_object_or_404(Person,pk=person_id)
        return render(request,"scammerlist/report.html",{"person":person, 'theme':theme})
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
    theme = request.session.get('theme',"css/bootstrap.min.css")
    people = Person.objects.all()
    return render(request,"scammerlist/report_detail.html",{"people":people, 'theme':theme})

    
def addperson(request):
    theme = request.session.get('theme',"css/bootstrap.min.css")
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
    return render(request,"scammerlist/add.html",{"catalog_all":catalog_all,'theme':theme})
    
def show_about(request):
    theme = request.session.get('theme',"css/bootstrap.min.css")
    return render(request,"scammerlist/about.html",{'theme':theme})
