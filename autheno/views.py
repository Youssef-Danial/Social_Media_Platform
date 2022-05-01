from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.utils import html
from django.contrib.auth.mixins import LoginRequiredMixin
from database.models import user, profile, file
from django.contrib.auth.hashers import make_password,check_password
import re
from main.relations import *
from main.post_comment import *
from autheno.forms import register, login_u
from django.views.generic.edit import FormMixin
from django.contrib import messages
from .cipher_auth import auth_user, is_user_auth, get_user, get_current_datetime
from autheno.filehandler import receive_files
# Create your views here.
class registery(FormMixin,View):
    def register(request):
        # if the user submit the form
        if request.method == 'POST':
        # create a form instance and populate it with data from the request:
            form = register(request.POST)
        # check whether it's valid:
            print(form.is_valid())
            if form.is_valid():
                u = form.save(False)
                password = form.cleaned_data.get("password")
                u.password_hash = make_password(password)
                del u.id
                del u._state
                # saving the user
                user_data = u.__dict__
                # adding the last login and the current date 
                user_data["last_login"] = get_current_datetime()
                user_data["created_date"] = get_current_datetime()
                new_user = user(**user_data)
                new_user.save()
                # creating a profile for the user 
                p = profile(user = new_user, link = "main/profile/"+str(new_user.id))
                f = file.objects.get(pk=10) # 10 the new user profile picture
                p.pfp = f
                p.save()
                # authenticting user after registering
                auth_user(request, new_user.email, password)
                # marking the user to be authenticated
                return HttpResponseRedirect(reverse_lazy("autheno:home"))
        else:
            form = register()
        
        return render(request, "authenticate/register.html", {"form":form})
    
    def register_action(self, request):
        pass

class login(View):

    def login(request):
        if request.method == 'POST':
            form = login_u(request.POST)
            if form.is_valid():
                client = form.cleaned_data
                u = user.objects.filter(email=client["email"]).first()
                if u != None:
                    if check_password(client["password"], u.password_hash):
                        # enter the homepage
                        # marking the user to be authenticated
                        auth_user(request, u.email, client["password"])
                        return HttpResponseRedirect(reverse_lazy("autheno:home"))
                    else:
                        # print a message wrong authentication 
                        messages.error(request, "Wrong Password or Email")
                else:
                    messages.error(request, "This email is not registered")
        else:
            form = login_u()   
            #request.session"] = None
        return render(request, "authenticate/login.html", {"form":form})

def create_poste(request):
        if is_user_auth(request):
            fileslist = receive_files(request, state="post")
            if request.method == "POST":
                # getting user data
                request.POST._mutable = True
                u = get_user(request)
                data = request.POST
                data["instance_name"] = u.user_name
                data["instance_id"] = u.id 
                if create_post(request, data, fileslist):
                    return HttpResponse("Posted successfully")
                else:
                    return HttpResponse("User is not authenticated")
            return fileslist
        return None


   
def home(request):
   
    if is_user_auth(request):
        # loading feeds for this user
        userposts = get_feeds(request)
        viewer = get_user(request)
        # reciving the file
        formfile = create_poste(request)
        #print("user is authenticated")
        # getting the user
        u = get_user(request)
        #return HttpResponseRedirect("https://www.google.com")
        return render(request, "authenticate/homepage.html", {"user": u, "formfile":formfile, "posts":userposts, "viewer":viewer.id})
    else:
        #print("not authenticated")
        return HttpResponseRedirect(reverse_lazy("autheno:login"))

def registere(request):
        # if the user submit the form
        if request.method == 'POST':
        # create a form instance and populate it with data from the request:
            form = register(request.POST)
        # check whether it's valid:
            print(form.is_valid())
            if form.is_valid():
                u = form.save(False)
                password = form.cleaned_data.get("password")
                u.password_hash = make_password(password)
                del u.id
                del u._state
                # saving the user
                user_data = u.__dict__
                # adding the last login and the current date 
                user_data["last_login"] = get_current_datetime()
                user_data["created_date"] = get_current_datetime()
                new_user = user(**user_data)
                new_user.save()
                # creating a profile for the user 
                p = profile(user = new_user, link = "main/profile/"+str(new_user.id))
                p.save()
                # authenticting user after registering
                auth_user(request, new_user.email, password)
                # marking the user to be authenticated
                return HttpResponseRedirect(reverse_lazy("autheno:home"))
        else:
            form = register()
        
        return form

def logine(request):
        if request.method == 'POST':
            form = login_u(request.POST)
            if form.is_valid():
                client = form.cleaned_data
                u = user.objects.filter(email=client["email"]).first()
                if u != None:
                    if check_password(client["password"], u.password_hash):
                        # enter the homepage
                        # marking the user to be authenticated
                        auth_user(request, u.email, client["password"])
                        return HttpResponseRedirect(reverse_lazy("autheno:home"))
                    else:
                        # print a message wrong authentication 
                        messages.error(request, "Wrong Password or Email")
                else:
                    messages.error(request, "This email is not registered")
        else:
            form = login_u()   
            #request.session"] = None
        return form

def login_register(request):
    register_form = registere(request)
    login_form = logine(request)
    return render(request, "authenticate/login-register.html", {"login_form":login_form, "register_form":register_form})

def logout(request): # loging out a user
    if is_user_auth(request):
        # loging the user out
        try:
            del request.session['email']
        except KeyError:
            pass
        return HttpResponse("You're logged out.")



