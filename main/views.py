from django.shortcuts import render
from django.views.generic import View
from autheno.cipher_auth import get_user, get_userbyid, user_equal, get_user_profile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from autheno.filehandler import receive_file
from database.models import file, profile as profilemodel, user
# Create your views here.
class profile(View):
    def get(self, request, user_id):
        #user = get_user(request)
        user = get_userbyid(user_id)
        is_owner = False
        prof = get_user_profile(user)
        temp = "1/profile/Picture1.png"
        if user != None:
            # show if the owner
            if user_equal(request, user):
                # you are the owner of the profile page
                is_owner = True
            # show if the viewer
            return render(request, "main/profile.html", {"user":user, "is_owner":is_owner, "profile": temp})
        else:
            return HttpResponse("The User you are looking for does not Exist")
    
    def edit_pfp(request):
        # creating a form for the profile picture
        pfp = receive_file(request, state="profile  ")
        u = get_user(request)
        if type(pfp) is file:
            # linking the file to the profile of the user
            p = profilemodel.objects.filter(user=u).first()
            # linking the profile pictre to the profile of the user
            p.pfp = pfp
            p.save()
            # chaging the state of the pfp
            return HttpResponseRedirect(reverse_lazy("main:profile", args = [u.id]))
        else:
            return render(request, "main/uploadfile.html", {"form":pfp, "user":u})