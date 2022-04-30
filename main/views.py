from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from autheno.cipher_auth import get_user, get_userbyid, is_user_auth, user_equal, get_user_profile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from autheno.filehandler import receive_file
from database.models import file, profile as profilemodel, user
from main.post_comment import load_profile_posts
from database.models import postfile
from main.relations import *
from main.notifications import *
from main.post_comment import *
import re
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
class profile(View):
    def get(self, request, user_id):
        #user = get_user(request)
        viewer = get_user(request)
        mutual = get_mutualfriends(request, user_id)
        user = get_userbyid(user_id)
        is_owner = False
        #temp = "1/profile/Picture1.png"
        prof = None
        # getting the data of the user states
        is_ufollower = is_follower(request, user_id)
        is_ufriend = is_friend(request, user_id)
        if is_user_auth(request):
            if user != None:
                # show if the owner
                prof = get_user_profile(user)
                if user_equal(request, user):
                    # you are the owner of the profile page
                    is_owner = True

                # loading profile posts that are who can see equal to followers
                
                # if owner it will show his all posts
                if is_owner == True:
                    # loading the onlyme profile posts that who can see equal to onlyme
                    profileposts = profile.load_profile_posts(request, user_id, state = "all")
                # checking if the user is a follower
                elif is_follower(request, user_id):
                    profileposts = profile.load_profile_posts(request, user_id, state="followers")
                else:
                    profileposts = profile.load_profile_posts(request, user_id, state="public")
                    #filesdictioanry.update(filesdictioanryonlyme)
                #print(filesdictioanry)
                # show if the viewer
                return render(request, "main/profile.html", {"user":viewer, "is_owner":is_owner, "profile": prof, "posts":profileposts, "is_follower":is_ufollower, "is_friend": is_ufriend, "mutual_friends":mutual, "viewer":viewer.id})
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
    def edit_backpfp(request):
        # creating a form for the profile picture
        pfpback = receive_file(request, state="profile")
        u = get_user(request)
        if type(pfpback) is file:
            # linking the file to the profile of the user
            p = profilemodel.objects.filter(user=u).first()
            # linking the profile pictre to the profile of the user
            p.pfpback = pfpback
            p.save()
            # chaging the state of the pfp
            return HttpResponseRedirect(reverse_lazy("main:profile", args = [u.id]))
        else:
            return render(request, "main/uploadfile.html", {"form":pfpback, "user":u})

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

def follow_friend(request):
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            # now receiving the post data
            userid = request.POST["user"]
            follow_user(request, userid)
        return JsonResponse({"nothing":None},status=200)

def unfollow_friend(request):
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            # now receiving the post data
            userid = request.POST["user"]
            unfollow(request, userid)
        return JsonResponse({"nothing":None},status=200)

def add_friend(request):
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            # now receiving the post data
            userid = request.POST["user"]
            print("you are wrong")
            send_friend_request(request, userid)
        return JsonResponse({"nothing":None},status=200)

def un_friend(request):
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            # now receiving the post data
            userid = request.POST["user"]
            print("userid : {}".format(userid))
            print("userid : {}".format(get_user(request).id))
            print(unfriend(request, userid))
        return JsonResponse({"nothing":None},status=200)

def show_notifications(request):
    # first we load the notifications
    user = get_user(request)
    print("request from view {}".format(request))
    notifs =  get_user_notifications(request, state="unread")
    print("notifications are ----------({})---------".format(len(notifs)))
    return render(request, "main/notification_s.html", {"notifs":notifs, "user":user})

def notif_markread(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called mark read notification")
            # now receiving the post data
            notif_id = request.POST["notif_id"]
            make_notification_read(request, notif_id)
        return JsonResponse({"nothing":None},status=200)

def accept_friend(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called accept friend request")
            # now receiving the post data
            user_id = request.POST["user_id"]
            accept_friendrequest(request, user_id)
            print("-----------{}----------accept".format(user_id))
        return JsonResponse({"nothing":None},status=200)

def reject_friend(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called reject friend request")
            # now receiving the post data
            user_id = request.POST["user_id"]
            print("-----------{}----------reject".format(user_id))
            reject_friendrequest(request, user_id)
        return JsonResponse({"nothing":None},status=200)

def like_post(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called reject friend request")
            # now receiving the post data
            post_id = request.POST["post_id"]
            add_react_post(request, post_id)
        return JsonResponse({"nothing":None},status=200)

def remove_like_post(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called reject friend request")
            # now receiving the post data
            post_id = request.POST["post_id"]
            remove_react_post(request, post_id)
        return JsonResponse({"nothing":None},status=200)

def show_settings(request):
    if (is_user_auth(request)):
        # code 
        # getting the user
        u = get_user(request)
        return render(request, "main/settings.html",{"user":u})

def clean_email(email):
    data = email
    if re.match(r"(?:^|\s)[\w!#$%&'*+/=?^`{|}~-](\.?[\w!#$%&'*+/=?^`{|}~-]+)*@\w+[.-]?\w*\.[a-zA-Z]{2,3}\b", data):
        pass
    else:
        return None
    # checking if the email already in the database
    u = user.objects.filter(email=data).first()
    if u == None:
        pass
    else:
        return None
    return data

def change_email(request):
    print("change email called")
    if is_user_auth(request):
        # now we get the user
        userinstance = get_user(request)
        if request.method == 'POST':
            new_email = clean_email(request.POST["email"])
            if new_email is not None:
                userinstance.email = new_email
                # saving the new email and returning success to the front
                userinstance.save()
                # authenticating the new email
                auth_user(request, userinstance.email, userinstance.password_hash)
                return JsonResponse({"feedback":"success"},status=200)
            else:
                # something wrong with the email returning error
                return JsonResponse({"feedback":"Wrong"},status=200)
    return JsonResponse({"feedback":"Nothing"},status=200)

def clean_username(username):
        data = username
        if re.match(r"^([ \u00c0-\u01ffa-zA-Z'\-])+$", data):
            pass
        else:
            return None
        # checking if there user with the same username in the database
        u = user.objects.filter(user_name=data).first()
        if u == None:
            pass
        else:
            raise None
        return data

def change_username(request):
    print("change username called")
    if is_user_auth(request):
        # now we get the user
        userinstance = get_user(request)
        if request.method == 'POST':
            new_username = clean_username(request.POST["username"])
            if new_username is not None:
                userinstance.user_name = new_username
                # saving the new email and returning success to the front
                userinstance.save()
                # authenticating the new email
                auth_user(request, userinstance.email, userinstance.password_hash)
                return JsonResponse({"feedback":"success"},status=200)
            else:
                # something wrong with the email returning error
                return JsonResponse({"feedback":"Wrong"},status=200)
    return JsonResponse({"feedback":"Nothing"},status=200)

def clean_phonenumber(phonenumber):
    # for the future
    return phonenumber

def change_phonenumber(request):
    print("change phonenumber called")
    if is_user_auth(request):
        # now we get the user
        userinstance = get_user(request)
        if request.method == 'POST':
            new_phonenumber = clean_phonenumber(request.POST["phonenumber"])
            if new_phonenumber is not None:
                userinstance.phone_number = new_phonenumber
                # saving the new email and returning success to the front
                userinstance.save()
                # authenticating the new email
                auth_user(request, userinstance.email, userinstance.password_hash)
                return JsonResponse({"feedback":"success"},status=200)
            else:
                # something wrong with the email returning error
                return JsonResponse({"feedback":"Wrong"},status=200)
    return JsonResponse({"feedback":"Nothing"},status=200)

def clean_password(password):
        cleaned_data = password
        # first checking if the password matchs
        # password = cleaned_data["password"]
        # passwordcon = cleaned_data["passwordconfirm"]
        # if password != passwordcon:
        #     raise forms.ValidationError(
        #         "password and confirm password does not match"
        #     )
        # checking the password if it is match the requirements
        if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", password):
            pass
        else:
            return None
        return cleaned_data 

def change_password(request):
    print("change password called")
    if is_user_auth(request):
        # now we get the user
        userinstance = get_user(request)
        if request.method == 'POST':
            new_password = clean_password(request.POST["newpassword"])
            old_password = request.POST["oldpassword"]
            if new_password is not None and check_password(old_password, userinstance.password_hash):
                userinstance.password_hash = make_password(new_password)
                # saving the new email and returning success to the front
                userinstance.save()
                # authenticating the new email
                auth_user(request, userinstance.email, userinstance.password_hash)
                return JsonResponse({"feedback":"success"},status=200)
            else:
                # something wrong with the email returning error
                return JsonResponse({"feedback":"Wrong"},status=200)
    return JsonResponse({"feedback":"Nothing"},status=200)

def edit_settings(request):
     # now sending the friend request
    if request.method == 'POST':
        print("called reject friend request")
        # now receiving the post data
        post_id = request.POST["post_id"]
        # here should be the edit profile function
    return JsonResponse({"nothing":None},status=200)