from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from autheno.cipher_auth import get_postbyid, is_user_auth, get_user
from autheno.filehandler import receive_files
from database.models import profile
from main.post_comment import *
from django.forms import Form
from django.views import View
# Create your views here.
def ajax_test(request):
    profileinstance = profile.objects.get(pk=1)
    aboutme = profileinstance.about_me
    return JsonResponse({"aboutme": aboutme})  
def ajax(request):
    return render(request, "testing/ajaxtest.html")  

def javascriptrender(request):
    return render(request, "testing/javascript.html")

class posts(View):
    def get(self, request, post_id):
        postinstance = load_post(request, post_id)
        if is_user_auth(request):
            data = {
                "post": postinstance,
                "is_owner": False
            }
            # checking if the user is permetted to see the post

            if is_post_owner(request, post_id):
                # should display edit and delete button
                data["is_owner"] = True
            # else it should display the post data

            return render(request,"testing/postdisplay.html",data)
        else:
            return HttpResponse("You are authenticated try loging in") 
    def create_post(request):
        if is_user_auth(request):
            fileslist = receive_files(request, state="post")
            if request.method == "POST":
                # getting user data
                request.POST._mutable = True
                u = get_user(request)
                data = request.POST
                data["instance_name"] = u.user_name
                data["instance_id"] = u.id 
                if create_post(request, data,fileslist):
                    return HttpResponse("Posted successfully")
                else:
                    return HttpResponse("User is not authenticated")
            return render(request, "testing/post.html",{"form":fileslist})
        return HttpResponse("User is not authenticated try to login")

    def disply_edit_post(request, post_id):
        if is_user_auth(request):
            if is_post_owner(request, post_id):
                # now he can edit the post
                # getting the post 
                postinstance = get_postbyid(post_id)
                data={
                    "post":postinstance
                }
                return render(request, "testing/editpost.html", data)
    def editpost(request, post_id):
        if is_user_auth(request):
            if is_post_owner(request, post_id):
                # now he can edit the post
                data = request.POST
                edit_post()
                return render(request, "testing/editpost.html", data)


    def post(self,request, post_id):
        print("create comment called ==========================----=-=-=-=-")
        print(is_user_auth(request))
        print("create comment called ==========================----=-=-=-=-")
        if is_user_auth(request):
            print("the function is called")
            fileslist = receive_files(request, state="comment")
            if request.method == "POST":
                # getting user data
                request.POST._mutable = True
                u = get_user(request)
                data = request.POST
                data["user"] = u
                if create_comment(request, data,fileslist):
                    HttpResponseRedirect(reverse("testing:displaypost", args=[int(data["post"])]))
                else:
                    return HttpResponse("User is not authenticated")
            print("file should show up")
            return HttpResponseRedirect(reverse("testing:displaypost", args=[post_id]))
        return HttpResponse("User is not authenticated try to login")