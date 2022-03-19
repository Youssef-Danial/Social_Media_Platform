from django.shortcuts import render
from django.views.generic import View
from autheno.cipher_auth import get_user, get_userbyid, is_user_auth, user_equal, get_user_profile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from autheno.filehandler import receive_file
from database.models import file, profile as profilemodel, user
from main.post_comment import load_profile_posts
from database.models import postfile
# Create your views here.
class profile(View):
    def get(self, request, user_id):
        #user = get_user(request)
        user = get_userbyid(user_id)
        is_owner = False
        #temp = "1/profile/Picture1.png"
        prof = None
        if is_user_auth(request):
            if user != None:
                # show if the owner
                prof = get_user_profile(user)
                if user_equal(request, user):
                    # you are the owner of the profile page
                    is_owner = True

                # loading profile posts that are who can see equal to followers
                
                # if owner it will show his all posts
                if not is_owner:
                    # loading the onlyme profile posts that who can see equal to onlyme
                    profileposts = profile.load_profile_posts(request, user_id, state = "followers")
                else:
                    profileposts = profile.load_profile_posts(request, user_id, state="all")
                    #filesdictioanry.update(filesdictioanryonlyme)
                #print(filesdictioanry)
                # show if the viewer
                print(profileposts)
                return render(request, "main/profile.html", {"user":user, "is_owner":is_owner, "profile": prof, "posts":profileposts})
            else:
                return HttpResponse("The User you are looking for does not Exist")
        else:
            # the user is login redirecting him to the login page
            return HttpResponseRedirect(reverse_lazy("autheno:login"))

    def edit_pfp(request):
        # creating a form for the profile picture
        pfp = receive_file(request, state="profile")
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
    
    def edit_about_me(request):
        about_me = request.POST.get("txt")
        user = get_user(request)
        prof = get_user_profile(user)
        prof.about_me = about_me
        prof.save()
        return HttpResponseRedirect(reverse_lazy("main:profile", args = [user.id]))
    
    def load_profile_posts(request, user_id, state):
        profileposts = load_profile_posts(request, user_id, state)
        return profileposts
    def send_friend_request(request):
        pass
