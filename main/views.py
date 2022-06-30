from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from autheno.cipher_auth import get_user, get_userbyid, is_user_auth, user_equal, get_user_profile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from autheno.filehandler import receive_file
from database.models import file, profile as profilemodel, user
from main.post_comment import load_profile_posts
from database.models import postfile, post_group, user_group
from main.relations import *
from main.notifications import *
from main.post_comment import *
import re
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
from main.page_group import *
# Create your views here.
class profile(View):
    def get(self, request, user_id):
        if is_user_auth(request):
            pass
        else:
            return HttpResponseRedirect(reverse_lazy("autheno:login-register"))
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
        if(is_blocked(request, user_id)):
            message = "You are blocked by this User"
            return render(request, "main/notify_page.html", {"user":viewer, "is_owner":is_owner, "profile": prof, "is_follower":is_ufollower, "is_friend": is_ufriend, "mutual_friends":mutual, "viewer":viewer.id,  "message":message})
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
                message = "The User you are looking for does not Exist"
                return render(request, "main/notify_page.html", {"user":viewer, "is_owner":is_owner, "profile": prof, "is_follower":is_ufollower, "is_friend": is_ufriend, "mutual_friends":mutual, "viewer":viewer.id,  "message":message})
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
            unfriend_request(request, userid)
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
            print("-----------{}----------accept".format(user_id))
            accept_friendrequest(request, user_id)
            
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

def like_comment(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called like comment")
            # now receiving the post data
            comment_id = request.POST["comment_id"]
            add_react_comment(request, comment_id)
        return JsonResponse({"nothing":None},status=200)

def remove_like_comment(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called remove like comment")
            # now receiving the post data
            comment_id  = request.POST["comment_id"]
            remove_react_comment(request, comment_id )
        return JsonResponse({"nothing":None},status=200)


def receive_newcomments(post_id, old_num_comments, commentslist,request):
    u = get_user(request)
    postinstance = get_postbyid(post_id)
    response = {}
    if postinstance.comment_number() > int(old_num_comments):
        response["newcomment"] = ""
        new_comment_number = postinstance.comment_number()
        response["newcommentnumber"] = new_comment_number
        newcommentslen = postinstance.comment_number() - int(old_num_comments)
        commentinstance = comment.objects.filter(post=postinstance).order_by('-id')[:newcommentslen]
        for commentin in commentinstance:
            rendered = render_to_string('main/comment.html', { 'comment': commentin,"viewer":u.id})
            response["newcomment"] += rendered
        return response
    if postinstance.comment_number() < len(commentslist):
        # doing the remove comment here
        commentslist = list(map(int, commentslist))
        commentslistfrompost = postinstance.get_comments()
        commentslistids = [commentin.id for commentin in commentslistfrompost]
        print(commentslist)
        print(commentslistids)
        set_difference = set(commentslist) - set(commentslistids)
        print(f"the difference {list(set_difference)}")
        response["deletedcomments"] = list(set_difference)
        return response
    responsew = {}
    return responsew

def get_list_from_POST(request):
    for item in request.POST.keys():
        items =  request.POST.getlist(item)
        if len(items) > 1:
            return list(items)
    return list()
def new_comments(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            # now receiving the post data
            comment_num  = request.POST["comment_num"]
            commentslist = get_list_from_POST(request)
            post_id = request.POST["post_id"]
            #print(f"{comment_num}, {post_id}")
            response = receive_newcomments(post_id,comment_num, commentslist, request)
            print(f"server response {response.keys()}")
        return JsonResponse(response,status=200)

def like_post(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called like post")
            # now receiving the post data
            post_id = request.POST["post_id"]
            add_react_post(request, post_id)
        return JsonResponse({"nothing":None},status=200)

def remove_like_post(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called remove like post")
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

def remove_post(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            post_id = request.POST["post_id"]
            print("-----------{}----------remove post".format(post_id))
            delete_post(request, post_id)
        return JsonResponse({"nothing":None},status=200)

def remove_comment(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            comment_id = request.POST["comment_id"]
            print("-----------{}----------remove comment".format(comment_id))
            delete_comment(request, comment_id)
        return JsonResponse({"nothing":None},status=200)


def block_friend(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called block")
            # now receiving the post data
            user_id = request.POST["user_id"]
            block_user(request, user_id)
        return JsonResponse({"nothing":None},status=200)
def unblock_friend(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            print("called unblock")
            # now receiving the post data
            user_id = request.POST["user_id"]
            # print("-----------{}----------remove post".format(user_id))
            unblock(request, user_id)
        return JsonResponse({"nothing":None},status=200)



def is_there_notifications(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            #print("called receive notification")
            # now receiving the post data
            oldvalue = request.POST["notifnum"]
            notificationsinstance = get_user_notifications(request, state="unread")
            response = {}
            if len(notificationsinstance)>0 and len(notificationsinstance)!=oldvalue:
                response["notifnum"] = len(notificationsinstance)
        return JsonResponse(response,status=200)


def edit_settings(request):
     # now sending the friend request
    if request.method == 'POST':
        print("called reject friend request")
        # now receiving the post data
        post_id = request.POST["post_id"]
        # here should be the edit profile function
    return JsonResponse({"nothing":None},status=200)

# searching part 
def searchfunc(request, content):
    #try:
        # making the search query to a lowercase for the search
        content = str(content).lower()
        usersearcher = get_user(request)
        # searching for a user
        userinstances = user.objects.all()
        tfidf_vectorizer = TfidfVectorizer(analyzer="char")
        user_resultlist = []
        for userinstance in userinstances:
            sparse_matrix = tfidf_vectorizer.fit_transform([content]+[str(userinstance.user_name).lower()])
            cosine = cosine_similarity(sparse_matrix[0,:],sparse_matrix[1:,:])
            if cosine[0][0] > 0.80:
                user_resultlist.append(userinstance)
        # searching for posts
        postinstances = post.objects.all()
        post_resultlist = []
        for postinstance in postinstances:
            sparse_matrix = tfidf_vectorizer.fit_transform([content]+[str(postinstance.text_content).lower()])
            cosine = cosine_similarity(sparse_matrix[0,:],sparse_matrix[1:,:])
            print(is_follower(request, postinstance.user.id))
            if cosine[0][0] > 0.80:
                if postinstance.post_location == "profile":
                    if  postinstance.who_can_see == "public" or is_follower(request, postinstance.user.id) or usersearcher.id == postinstance.user.id:
                        print("enteredone")
                        post_resultlist.append(postinstance)
        groupinstances = group.objects.all()
        group_resultlist = []
        for groupinstance in groupinstances:
            sparse_matrix = tfidf_vectorizer.fit_transform([content]+[str(groupinstance.description).lower() + str(groupinstance.name).lower()])
            cosine = cosine_similarity(sparse_matrix[0,:],sparse_matrix[1:,:])
            if cosine[0][0] > 0.50:
                group_resultlist.append(groupinstance)
        return (user_resultlist, post_resultlist, group_resultlist)
    #except:
        #return None

def get_search(request):
    # we mark the notification as read
    if (is_user_auth(request)):
        query = request.GET.get('q','')
        userinstance = get_user(request)
        userlist = []
        postlist = []
        grouplist = []
        if query:
            userlist, postlist,grouplist = searchfunc(request, query)
        data={
                "userlist":userlist,
                "postlist":postlist,
                "grouplist":grouplist,
                "user":userinstance,
                "profile":userinstance.profile,
                "viewer":userinstance.id,
            }
        return render(request, "main/search.html", data)

def get_user_groups(request):
    userinstance = get_user(request)
    # checking the groups of that user
    user_groupinstance = user_group.objects.filter(user = userinstance)
    grouplist = []
    for usergroupinstance in user_groupinstance:
        grouplist.append(usergroupinstance.group)
    return grouplist

def get_user_created_groups(request):
    userinstance = get_user(request)
    groupinstances = group.objects.filter(creator = userinstance)
    group_createdlist = []
    for groupins in groupinstances:
        group_createdlist.append(groupins)
    return group_createdlist
    
def friends(request):
     # we mark the notification as read
    if (is_user_auth(request)):
        userinstance = get_user(request)
        # getting the user friends and followers
        userinstanceid = userinstance.id
        userfriends = get_friendlist(userinstanceid)
        friendslist = []
        for friend in userfriends:
            if friend.sender_id == userinstanceid:
                friendslist.append(get_userbyid(friend.receiver_id))
            else:
                friendslist.append(get_userbyid(friend.sender_id))
        # handling followers
        followers = get_followers(userinstanceid)
        followerslist = []
        if followers is not None:
            for follower in followers:
                followerslist.append(follower.follower)
        #print(friendslist[0].user_name)
        grouplist = get_user_groups(request)
        groupcreatedlist = get_user_created_groups(request)
        data = {
            "user":userinstance,
            "viewer": userinstance.id,
            "userfriends":friendslist,
            "followerslist":followerslist,
            "grouplist": grouplist,
            "groupscreated": groupcreatedlist,
        }
        return render(request, "main/friends.html", data)
    else:
        return HttpResponse("You are not authorized try logining in")
# group section
def get_group_posts(groupinstance):
    grouppostslist = []
    groupposts = post_group.objects.filter(group = groupinstance)
    for grouppost in groupposts:
        grouppostslist.append(grouppost.post)
    return reversed(grouppostslist)

def create_postee(request):
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
class groupe(View):
    def get(self, request, group_id):
        if is_user_auth(request):
             #user = get_user(request)
            viewer = get_user(request)
            groupinstance  = get_groupbyid(group_id)
            groupposts = get_group_posts(groupinstance)
            formfile = create_postee(request)
            data = {
                "group":groupinstance,"formfile":formfile,"user":viewer, "posts":groupposts, "viewer":viewer.id
            }
            return render(request,"main/group.html",data)
        else:
            return HttpResponseRedirect(reverse_lazy("autheno:login-register"))
    

def create_group(request):
    if (is_user_auth(request)):
        data = {}
        # getting user who sent the request
        userinstance = get_user(request)
        data["creator"] = userinstance
        data["name"] = request.POST.get("groupname")
        data["description"]= request.POST.get("groupdesc")
        ispublic = request.POST.get("ispublic")
        print(ispublic)
        if (ispublic == "public"):
            data["is_public"] = True
        else:
            data["is_public"] = False
        data ["state"] = "working" # empty for now it is not being used
        print(data)
        if create_groupfunc(request, data):
            return JsonResponse({"feedback":"success"},status=200)
        else:
            return JsonResponse({"nothing":None},status=200)


def is_group_CorM(userid,groupid): # checking if the user is moderator or creator of the page
    try:
        userinstance = get_userbyid(userid)
        groupinstance = get_groupbyid(groupid)
        user_group_instance = user_group.objects.filter(user = userinstance, group=groupinstance).first()
        if  groupinstance.creator == userinstance: 
            return True
        elif user_group_instance != None and user_group_instance.state == "moderator":
            return True
        else:
            return False
    except:
       return False

def get_group_mods(request, group_id):
    try:
        if is_user_auth(request):
            if is_group_creator(request, group_id) or is_usergroup_moderator(request, group_id):
                # making sure that the information only appears for creator or moderator of the group
                group_instance = get_groupbyid(group_id)
                user_group_instances = user_group.objects.filter(group=group_instance, state = "moderator")
                return user_group_instances
            else:
                return None
        else:
            return None
    except:
        return None

def get_banned_users(request, group_id):
    try:
        if is_user_auth(request):
            if is_group_creator(request, group_id) or is_usergroup_moderator(request, group_id):
            #if True:
                # making sure that the information only appears for creator or moderator of the group
                group_instance = get_groupbyid(group_id)
                user_group_instances = user_group.objects.filter(group=group_instance, user_state = "refused")
                return user_group_instances
            else:
                return None
        else:
            return None
    except:
        return None
class group_settings(View):
    def get(self, request, group_id):
        userinstance = get_user(request)
        groupinstance = get_groupbyid(group_id)
        if (is_user_auth(request) and is_group_CorM(userinstance.id,groupinstance.id)):
            moderatorlist = get_group_mods(request, group_id)
            grouprequests = get_group_requests(request, group_id)
            groupusers = get_group_users(request, group_id)
            banned_users = get_banned_users(request, group_id)
            print(banned_users)
            data = {"user": userinstance,
            "group":groupinstance,
            "mods":moderatorlist,
            "grouprequests":grouprequests,
            "groupusers":groupusers,
            "banned_users": banned_users}
            return render(request, "main/groupsettings.html", data)

# user
def create_group_request(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            group_id = request.POST["group_id"]
            print("-----------{}----------joining group".format(group_id))
            join_group(request, group_id)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

def remove_group_request(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            group_id = request.POST["group_id"]
            print("-----------{}----------leaving group".format(group_id))
            leave_group(request, group_id)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

def remove_group_requestban(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            groupuserid = request.POST["request_id"]
            groupuserinstance = user_group.objects.get(pk=groupuserid)
            user_id = groupuserinstance.user.id
            group_id = groupuserinstance.group.id
            #objectinstance = object.objects.get(pk=7)
            print("-----------{}----------removing user group".format(group_id))
            unban(user_id, group_id)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

# admin or moderator
def accept_group_request(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            groupuserid = request.POST["request_id"]
            groupuserinstance = user_group.objects.get(pk=groupuserid)
            user_id = groupuserinstance.user.id
            group_id = groupuserinstance.group.id
            #objectinstance = object.objects.get(pk=7)
            print("-----------{}----------accepting group".format(group_id))
            add_user_to_group(request, user_id, group_id, "groupaccept")
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

def remove_user_group(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            groupuserid = request.POST["request_id"]
            groupuserinstance = user_group.objects.get(pk=groupuserid)
            user_id = groupuserinstance.user.id
            group_id = groupuserinstance.group.id
            #objectinstance = object.objects.get(pk=7)
            print("-----------{}----------removing user group".format(group_id))
            refuse_group_request(user_id, group_id)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

def refuse_group_requestt(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            groupuserid = request.POST["request_id"]
            groupuserinstance = user_group.objects.get(pk=groupuserid)
            user_id = groupuserinstance.user.id
            group_id = groupuserinstance.group.id
            #objectinstance = object.objects.get(pk=7)
            print("-----------{}----------removing user group".format(group_id))
            leave_groupp(user_id, group_id)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

# getting ban and moderators
def make_mod(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            groupuserid = request.POST["request_id"]
            groupuserinstance = user_group.objects.get(pk=groupuserid)
            user_id = groupuserinstance.user.id
            group_id = groupuserinstance.group.id
            #objectinstance = object.objects.get(pk=7)
            print("-----------{}----------makeing mod user group".format(group_id))
            make_user_mod_group(request, user_id, group_id)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

def remove_mod(request):
    if is_user_auth(request):
         if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            groupuserid = request.POST["request_id"]
            groupuserinstance = user_group.objects.get(pk=groupuserid)
            user_id = groupuserinstance.user.id
            group_id = groupuserinstance.group.id
            #objectinstance = object.objects.get(pk=7)
            print("-----------{}----------removing user group".format(group_id))
            remove_user_mod_group(request, user_id, group_id)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

global_group = 0
class change_group_pfp(View):
    def get(self, request, group_id):
        try:
            global global_group
            global_group = group_id  
            groupinstance = group.objects.get(pk=group_id)
            pfp = receive_file(request, state="profile")
            u = get_user(request)
            return render(request, "main/uploadfilegroup.html", {"form":pfp,"group":groupinstance ,"user":u})
        except:
            return HttpResponse("Something Wrong with the Path")
        #return HttpResponse("unathenticated")
    def post(self, request, group_id):
        u = get_user(request)
        if is_user_auth(request) and is_group_CorM(u.id, group_id):
            print("in the function")
            # creating a form for the profile picture
            pfp = receive_file(request, state="profile")
            u = get_user(request)
            if type(pfp) is file:
                # linking the file to the profile of the user
                groupinstance = group.objects.get(pk=group_id)
                # linking the profile pictre to the profile of the user
                groupinstance.grouppfp = pfp
                groupinstance.save()
                # chaging the state of the pfp
                return HttpResponseRedirect(reverse_lazy("main:group", args = [group_id]))
            else:
                return HttpResponse("unathenticated")

def edit_group_desc(request):
    textnew = request.POST.get("txt")
    group_id = request.POST.get("groupidd")
    groupinstance = group.objects.get(pk=int(group_id))
    groupinstance.description = textnew
    groupinstance.save()
    return HttpResponseRedirect(reverse_lazy("main:group", args = [groupinstance.id]))
    

def delete_groupp(request):
    if is_user_auth(request):
        if request.method == 'POST':
            print("called remove post")
            # now receiving the post data
            groupid = request.POST["request_id"]
            #objectinstance = object.objects.get(pk=7)
            print("-----------{}----------removing user group".format(groupid))
            delete_group(request, groupid)
            return JsonResponse({"nothing":None},status=200)
    return HttpResponse("unathenticated")

# forget password 

def get_user_by_email(email):
    try:
        userinstance = user.objects.filter(email=email).first()
        return userinstance
    except:
        return None

def forget_password(request):
    if request.method == 'POST':
        tempemail = request.POST["useremail"]
        request.session["tempemail"] = tempemail
        print(tempemail)
        userinstance = get_user_by_email(tempemail)
        if userinstance != None:
            return JsonResponse({"success":"true"},status=200)
        else:   
            return JsonResponse({"success":"false"},status=200)


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import randint

def sendemail(receive_email):
    #tempcode = random_with_N_digits(8)
    tempcode = random_with_N_digits(randint(8, 16))
    #The mail addresses and password
    sender_address = 'spaceshareservices@gmail.com'
    sender_pass = 'vafqssdoazmnbgae'
    receiver_address = receive_email
    # getting user name with email
    userins = get_user_by_email(receive_email)
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f'Changing Password'   #The subject line
    mail_content = f'''
    Greetings {userins.user_name},
    This is your Verification Code it will expire with your session {tempcode}
    '''
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return tempcode


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def forget_passwordtwo(request):
    #password = "Testingspaceshare1"
    #secondpass = "vafqssdoazmnbgae"
    #email = "spaceshareservices@gmail.com"
    receive_email = request.session["tempemail"]
    temp_code = sendemail(receive_email)
    request.session["temp_code"] = temp_code
    return render(request, "main/forgetpassword.html")

def change_passwordtwo(request):
    print("change password called")
    if "tempemail" in request.session :
        # now we get the user
        tempmailtemp = request.session["tempemail"]
        userinstance = get_user_by_email(tempmailtemp)
        if request.method == 'POST':
            new_password = clean_password(request.POST["newpassword"])
            tempcodereceived = request.POST["oldpassword"]
            temp_code = request.session["temp_code"] 
            print(f"received code {tempcodereceived}")
            print(f"what we have code {temp_code}")
            if new_password is not None and str(temp_code) == str(tempcodereceived):
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