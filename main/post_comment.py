from sklearn.decomposition import TruncatedSVD
from main import relations
from autheno.cipher_auth import *
import datetime
from django.utils import timezone
from django.db.models import Q
from database.models import post, comment, postfile, post_react, comment_react, commentfile, postfile
from autheno.filehandler import receive_files
from autheno.cipher_auth import is_user_auth
from itertools import chain
from main.relations import is_follower, get_follows, get_friendlist, get_followers
from main.notifications import create_notification
# getting current Time
currentDateTime = datetime.datetime.now(tz=timezone.utc)


# post
def create_post(request, data, fileslist): # data should be a dictionary 
    # 100 percent if this function is called the user is already authenticated
    if is_user_auth(request):
        # getting the user that will make the post
        postuser = get_user(request)
        # data(text_content,)
        # adding missing parts from the data
        # create post object 
        p = post(user=postuser)
        p.text_content = data["text_content"] # saving the text content to the post
        p.who_can_see = data["who_can_see"]
        p.interaction_counter = "{likes:0}"
        p.post_location = data["post_location"]
        p.instance_id = data['instance_id']
        p.instance_name = data["instance_name"]
        # saving the post so we can receive the files
        p.create_date = get_current_datetime()
        p.save()
        if type(fileslist) is list:
            for file in fileslist:
                # marking the files to the post
                file.post = p
                file.save()
        # now creating a notifcation for other users
        # first we get the users who follow that person
        userfollowers = get_followers(p.user.id)
        print(f" the user post is called and {type(userfollowers)}")
        if userfollowers is not None and p.who_can_see != "onlyme":
            for followerinstance in userfollowers:
                print("the loop is working")
                create_notification(p.user.id, followerinstance.follower.id,'newpost', source=p.user.id, source_name = "user")
        return True
    else:
        return False


def load_profile_posts(request, user_id, state):
    if is_user_auth(request):
        # get the user_id posts
        u = get_userbyid(user_id)
        profileposts = None
        if state == "all":
            profileposts = post.objects.filter(user=u,post_location="profile").order_by("-create_date")
        elif state == "followers":
            print("follower")
            profileposts = post.objects.filter(Q(who_can_see="public")|Q(who_can_see="followers"),user=u,post_location="profile").order_by("-create_date")
        elif state == "public":
            profileposts = post.objects.filter(user=u,post_location="profile", who_can_see = "public").order_by("-create_date")
        #filedictionary = load_files(profileposts)
        return profileposts
    
def load_page_posts(request, page_id, state):
    pass

def load_group_posts(request, group_id, state):
    pass

def load_post(request, post_id):
    pass # here i need to check if the user is a follower or public
    try:
        post = get_postbyid(post_id)
        if  post.who_can_see == "public":
            return post
        elif is_post_owner(request ,post_id):
            return post
        elif is_follower(request, post.user.id) and post.who_can_see != "onlyme":
            return post
        else:
            return None
    except:
        return None
def edit_post(request, post_id, data, fileslist):
    try:
        if is_user_auth(request):
            if is_post_owner(request,post_id):
                # getting post with id 
                postinstance = get_postbyid(post_id)
                # post new data
                postinstance.text_content = data["text_content"]
                postinstance.edit_date = get_current_datetime() # updating the edit date
                postinstance.who_can_see = data["who_can_see"]
                # removing postfiles and receiving the files
                if len(fileslist) > 0: # for now user have to reupload files if he wants to edit
                    for file in postinstance.postfiles: 
                        file.delete()
                    if type(fileslist) is list:
                        for file in fileslist:
                          # marking the files to the post
                            file.post = postinstance
                            file.save()
    except:     
        pass

def delete_postfile(request, post_id):
    pass

def delete_post(request, post_id):
    try:
        postinstance = get_postbyid(post_id)
        if is_user_auth(request):
            if is_post_owner(request, post_id) or  postinstance.post_location == "group":
                postinstance = get_postbyid(post_id)
                postinstance.delete()
                return True
            return False # not the owner of the post
        return False # not authenticated
    except:
        return False

def create_comment(request, data, fileslist,comment_position = "main"): # comment position for main and reply comments to distinguish
    try:
        #
        if is_user_auth(request):
            userinstance = get_user(request)
            postinstance = get_postbyid(data["post"])
            commentinstance = comment(user = userinstance, post=postinstance)
            commentinstance.date = get_current_datetime()
            commentinstance.content = data["content"]
            commentinstance.save()
            create_notification(userinstance.id, postinstance.user.id,'commentpost', source=userinstance.id, source_name = "user")
            # now preparing the data
            # if type(fileslist) is list:
            #     for file in fileslist:
            #         # marking the files to the post
            #         file.comment = commentinstance
            #         file.save()
            # comment created
            return True
        return False
    except:
        return False

def edit_comment(request, comment_id):
    pass

def delete_comment(request, comment_id):
    try:
        if is_user_auth(request):
            if is_comment_owner(request, comment_id):
                print(f"delete the comment called --------------del")
                commentinstance = get_commentbyid(comment_id)
                commentinstance.delete()
                return True
            return False # not the owner of the post
        return False # not authenticated
    except:
        return False

def get_user_related(request):
    # this function should have the first part of the get_feeds function
    pass

def get_feeds(request):
    #try:
        userinstance = get_user(request)
        # getting follows
        follows = get_follows(request)
        # getting friends 
        friends = get_friendlist(userinstance.id)
        # getting the users from the friends and follows
        userslist = []
        for followinstance in follows:
            userslist.append(followinstance.followed)
        
        for friendinstance in friends:
            if friendinstance.sender != userinstance:
                userslist.append(friendinstance.sender)
            else:
                userslist.append(friendinstance.receiver)
        # now getting the posts that these users have made
        postslist = []
        for userins in userslist:
            # not getting user posts
            userposts = load_profile_posts(request, userins.id, state="followers")
            postslist.append(userposts)
        # now loading the user itself posts
        userposts = load_profile_posts(request, userinstance.id, state="followers")
        # now combining the posts and sorting it with date
        total_posts = userposts
        for posts in postslist:
            total_posts = total_posts | posts
        # ordering the posts
        total_posts = total_posts.order_by("-create_date")
        return total_posts
    #except:
    #   return False
def is_post_owner(request, post_id):
    try:
        # checking if the user is the owner of the post
        userinstance = get_user(request)
        post_instance = get_postbyid(post_id)
        if post_instance.user == userinstance:
            return True
        else:
            return False
    except:
        return False
def is_comment_owner(request, comment_id):
    try:
        userinstance = get_user(request)
        # postinstance = get_postbyid(post_id)
        commentinstance = get_commentbyid(comment_id)
        if commentinstance.user == userinstance:
            return True
        else:
            return False
    except:
        return False

def add_react_post(request, post_id, react="like"): # react type for now is like
    try:
        # checking if the user is authenticated
        if is_user_auth(request): # should return true if the user is authenticated
            # first we get the user and the post 
            userinstance  = get_user(request)
            
            postinstance = get_postbyid(post_id)
            print("===================")
            print(postinstance.user)
            # now adding a reaction to the post by loading the post_react model and inserting the new instance
            post_react_instance = post_react(user = userinstance, post = postinstance) # the default is set for like for now
            # now saving the post_react_instance to the databsae
            post_react_instance.save()
            create_notification(userinstance.id, postinstance.user.id,'postlike', source=userinstance.id, source_name = "user")
            return True
        return False
    except:
        return False # something wrong with the user or the post or the user is not authenticated

def remove_react_post(request, post_id, react="like"): # react type for now is like
    try:
        # checking if the user is authenticated
        if is_user_auth(request) and is_user_reacted_post(request, post_id): # should return true if the user is authenticated and if the user is reacted to this post
            # first we get the user and the post 
            userinstance  = get_user(request)
            postinstance = get_postbyid(post_id)
            # now removing a reaction to the post by loading the post_react model and inserting the new instance
            post_react_instance = post_react.objects.filter(user = userinstance, post = postinstance).first() # the default is set for like for now
            # now checking if there is a reaction or not
            post_react_instance.delete()
            return True
        return False # the user is not authenticated or did not react to the post at first place
    except:
        return False # something wrong with the user or the post
def add_react_comment(request, comment_id, react="like"): # react type for now is like
    try:
        if is_user_auth(request):
            userinstance = get_user(request)
            commentinstance = get_commentbyid(comment_id)
            comment_react_instance = comment_react(user = userinstance, comment = commentinstance)
            # now saving the comment_react_instance
            comment_react_instance.save()
            create_notification(userinstance.id, commentinstance.user.id,'commentlike', source=userinstance.id, source_name = "user")
            return True
        return False
    except:
        return False

def remove_react_comment(request, comment_id, react="like"): # react type for now is like
    try:
        if is_user_auth(request) and is_user_reacted_comment(request, comment_id):
            userinstance = get_user(request)
            commentinstance = get_commentbyid(comment_id)
            comment_react_instance = comment_react.objects.filter(user = userinstance, comment = commentinstance).first()
            # now deleting the comment_react_instance
            comment_react_instance.delete()
            return True
        return False
    except:
        return False

def is_user_reacted_post(request, post_id): # to check if the user reacted or not to the post so he could not react again
    # getting  the user and the post
    try:
        userinstance = get_user(request)
        postinstance = get_postbyid(post_id)
        post_react_instance = post_react.objects.filter(user = userinstance, post = postinstance).first() # the default is set for like for now
        if post_react_instance != None:
            return True # mean the user reacted to the post
        else:
            return False # the user did not react to the post
    except:
        return False # there something wrong with the user or the post maybe the do not exist
def is_user_reacted_comment(request, comment_id):
    try:
        userinstance = get_user(request)
        commentinstance = get_commentbyid(comment_id)
        # checking in the database 
        comment_react_instance = comment_react.objects.filter(user = userinstance, comment=commentinstance).first()
        if comment_react_instance != None:
            return True # mean the user reacted to the comment
        return False # the user did not react to the comment
    except:
        return False # there something wrong with the user or the comment maybe the do not exist

def num_reacts(request, post_id):
    userinstance  = get_user(request)
    postinstance = get_postbyid(post_id)
    post_react_instance = post_react.objects.filter(post = postinstance).values() # the default is set for like for now
    return len(post_react_instance)

# later
