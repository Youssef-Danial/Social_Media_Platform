from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from autheno.cipher_auth import is_user_auth, get_user
from autheno.filehandler import receive_files
from database.models import profile
from main.post_comment import create_post
from django.forms import Form
# Create your views here.
def ajax_test(request):
    profileinstance = profile.objects.get(pk=1)
    aboutme = profileinstance.about_me
    return JsonResponse({"aboutme": aboutme})  
def ajax(request):
    return render(request, "testing/ajaxtest.html")  

def javascriptrender(request):
    return render(request, "testing/javascript.html")

def post(request):
    if is_user_auth(request):
        fileslist = receive_files(request, state="post")
        if request.method == "POST":
            # getting user data
            u = get_user(request)
            data = request.POST
            data["instance_name"] = u.username
            data["instance_id"] = u.id 
            if create_post(request, data,fileslist):
                return HttpResponse("Posted successfully")
            else:
                return HttpResponse("User is not authenticated")
        return render(request, "post.html",{"form":fileslist})
    return HttpResponse("User is not authenticated try to login")