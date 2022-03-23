from main import relations
from autheno.cipher_auth import *
import datetime
from django.utils import timezone
from django.db.models import Q
from database.models import post, comment, postfile
from autheno.filehandler import receive_files
from autheno.cipher_auth import is_user_auth
from itertools import chain
# getting current Time
currentDateTime = datetime.datetime.now(tz=timezone.utc)


# post
def create_post(request, data, fileslist): # data should be a dictionary 
    # 100 percent if this function is called the user is already authenticated
    if is_user_auth(request):
        # getting the user that will make the post
        postuser = get_user(request)
        # data(text_content, )
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
        p.create_date = currentDateTime
        p.save()
        if type(fileslist) is list:
            for file in fileslist:
                # marking the files to the post
                file.post = p
                file.save()
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
        if is_user_auth(request):
            if is_post_owner(request, post_id):
                postinstance = get_postbyid(post_id)
                postinstance.delete()
                return True
            return False # not the owner of the post
        return False # not authenticated
    except:
        return False

def create_comment(request):
    pass

def edit_comment(request):
    pass

def delete_comment(request):
    pass

def get_feeds(request):
    pass

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