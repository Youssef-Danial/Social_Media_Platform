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

def load_files(posts):
    filedictionary = {} # post is the key files are the value
    for post in posts:
        fileslist = postfile.objects.filter(post = post).values()
        filedictionary[post.id] = fileslist
    return filedictionary

def load_profile_posts(request, user_id, state):
    if is_user_auth(request):
        # get the user_id posts
        u = get_userbyid(user_id)
        if state != "all":
            profileposts = post.objects.filter(user=u,post_location="profile", who_can_see = state).order_by("-create_date")
        else:
            profileposts = post.objects.filter(user=u,post_location="profile").order_by("-create_date")
        #filedictionary = load_files(profileposts)
        return profileposts