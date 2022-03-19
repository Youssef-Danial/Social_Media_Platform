from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
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
        postinstance = get_postbyid(post_id)
        print(postinstance)
        if is_user_auth(request):
            data = {
                "post": postinstance,
                "is_owner": False
            }
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

    def display_post(request, post_id):
        pass