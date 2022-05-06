from pyexpat import model
from django.db import models
from sqlalchemy import null
from datetime import datetime, timedelta
import datetime
from django.contrib.humanize.templatetags import humanize
from django.utils import timezone
from django.db.models import Q
currentDateTime = datetime.datetime.now(tz=timezone.utc)
# Create your models here.
import datetime


# some code
def get_postbyid(post_id):
    try:
        postinstance = post.objects.get(pk=post_id)
        return postinstance
    except:
        return None


def get_user(request):
    user_email = request.session.get('email')
    u = user.objects.filter(email=user_email).first()
    return u
    

def get_userbyid(user_id):
    try:
        u = user.objects.get(pk=user_id)
        return u
    except:
        return None



def get_friendlist(user_id): # this function should return a list of friend objects
    user = get_userbyid(user_id)
    # seraching for the friends of this user
    friendinstance = friendship.objects.filter(Q(sender_id = user) | Q(receiver_id = user), state="accepted").values()
    if friendinstance != None:
        return friendinstance
    else:
        return ""

def get_followers(user_id):
    # checking the followers of the userid
    user = get_userbyid(user_id)
    followinstance = follow.objects.filter(followed = user).values()
    # checking if the user have followers
    if len(followinstance) > 0:
        return followinstance
    else:
        return "" # there is no users following the given user

def get_user_notifications(userinstance, state="unread"):
    # try:
        
        # now searching and getting all the notifications that have been sent to this user
        if state =="unread":
            notifications = notification.objects.filter(receipt = userinstance, is_read = False).order_by("-time_sent")
            return notifications
        elif state == "read":
            notifications = notification.objects.filter(receipt = userinstance, is_read = True).order_by("-time_sent")
            return notifications
        else: # this mean all the notifications
            print(userinstance.id)
            notifications = notification.objects.filter(receipt = userinstance).order_by('-time_sent')
            return notifications
# model classes
class user(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=70, unique=True)
    password_hash = models.CharField(max_length=72)
    phone_number = models.CharField(max_length=50) #  unique=True do not forget to make the phone number unique
    birthdate = models.DateField()
    last_login = models.DateTimeField(null=True,blank=True)
    last_logout = models.DateTimeField(null=True,blank=True)
    is_verified = models.BooleanField(null=True, default=None)
    created_date = models.DateTimeField() # this null should be removed it is added because of makemigrations
    Lt_t_un_changed = models.DateTimeField(null=True,blank=True) # last time the username have been changed his name
    #profile_link = models.CharField()
    def get_notif_num(self):
        notifnum = get_user_notifications(self)
        return len(notifnum)
class file(models.Model):
    file_name = models.CharField(max_length=250)
    uploaded_date = models.DateTimeField()
    file_url = models.CharField(max_length=250)
    is_used = models.BooleanField(default=True) # state value if true the file is in use else it is not being used
class profile(models.Model):
    about_me = models.TextField(max_length=100)
    pfp = models.ForeignKey("file",on_delete=models.SET_NULL,null=True, related_name="pfp")
    pfpback = models.ForeignKey("file",on_delete=models.SET_NULL,null=True, related_name ="pfpback")
    link = models.URLField()
    user = models.OneToOneField("user", on_delete=models.CASCADE)
    def get_friends_num(self):
        friend_list = get_friendlist(self.user.id)
        return len(friend_list)
    def get_followers_num(self):
        followers_list = get_followers(self.user.id)
        return len(followers_list)

class object(models.Model):
    name = models.CharField(max_length=20, unique=True)
    text = models.CharField(max_length=100)

class notification(models.Model):
    receipt = models.ForeignKey("user", on_delete=models.SET_NULL,blank=True, null = True, related_name="receipt")
    sender = models.ForeignKey("user", on_delete=models.SET_NULL,blank=True, null = True, related_name="senderr")
    object_type = models.ForeignKey("object", on_delete=models.SET_NULL, null = True)
    source = models.CharField(max_length = 250, blank=True, null=True) # source id can be (group, comment, post, thread, user)
    source_name = models.CharField(max_length = 250, blank=True, null=True)
    time_sent = models.DateTimeField(blank=True,null=True)
    time_read = models.DateTimeField(blank=True,null=True)
    is_read = models.BooleanField(default=False)
    def get_source(self):
        if self.source_name == "user":
            try:
                u = user.objects.get(pk=int(self.source))
                return u
            except:
                return None
    def get_time(self):
        newtime = self.time_sent +  timedelta(hours=2)
        return newtime
class setting_code(models.Model):
    setting_name = models.CharField(max_length=50)
    default_value = models.CharField(max_length=20)

class user_settings(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    setting_code = models.ForeignKey("setting_code", on_delete=models.SET_NULL, null=True)
    value = models.CharField(max_length=20)
    modify_date = models.DateTimeField()

class post(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    create_date = models.DateTimeField()
    edit_date = models.DateTimeField(null = True, blank=True)
    text_content = models.TextField()
    # video = models.ForeignKey("video", on_delete=models.SET_NULL, null=True)
    who_can_see = models.TextField() # can be (followers, public, onlyme)
    interaction_counter = models.CharField(max_length=50) # this should be dictionary of keys(reactiontype): values(number of reaction)
    # post_state = models.IntegerField() #
    post_location = models.CharField(max_length=7) # this should be (profile, page, group)
    def get_files(self):
        return postfile.objects.filter(post=self).values()
    postfiles=property(get_files)
    instance_id = models.IntegerField() # can be (userid, groupid, pageid)
    instance_name = models.CharField(max_length=30) # this should be a name of a(user, page, group)
    def get_timeago(self):
        return humanize.naturaltime(self.create_date)

    def comment_number(self): # this will return the number of comments
        comment_instance = comment.objects.filter(post = self).values() # getting the comments
        return len(comment_instance)
    def get_comments(self):
        comments = comment.objects.filter(post=self)
        return comments
    def get_reactions(self):
        post_react_instance = post_react.objects.filter(post = self).values()
        return len(post_react_instance)
class postfile(models.Model):
    file_name = models.CharField(max_length=250)
    uploaded_date = models.DateTimeField()
    file_url = models.CharField(max_length=250)
    is_used = models.BooleanField(default=True) # state value if true the file is in use else it is not being used
    post = models.ForeignKey("post", on_delete=models.SET_NULL, blank=True, null=True)
    file_extension = models.CharField(max_length=6, null=True, blank=True)
    file_type = models.CharField(max_length = 6, blank=True, null=True) # this should be file type (audio, video, image, unkow) unknown

class post_react(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default = "like") # could be (like) this for future upgrades to the reaction between the user and the post
# class video(models.Model):
#     name=models.CharField(max_length=50)
#     video_url = models.TextField()
#     state = models.CharField(max_length=10) # have a state censored or deleted
#     is_used = models.BooleanField(default=True) # state value if true the file is in use else it is not being used
class comment(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField()
    edit_date = models.DateTimeField(null=True)
    interaction_counter = models.CharField(max_length=50, null =True)
    comment_position = models.CharField(max_length=5, default = "main") # this can be (main, reply) this is for reply comments
    def get_files(self):
        return commentfile.objects.filter(comment=self).values()
    commentfiles=property(get_files)
    def get_timeago(self):
        return humanize.naturaltime(self.date)
    def get_reactions(self):
        comment_react_instance = comment_react.objects.filter(comment = self).values()
        return len(comment_react_instance)
class commentfile(models.Model):
    file_name = models.CharField(max_length=250)
    uploaded_date = models.DateTimeField()
    file_url = models.CharField(max_length=250)
    is_used = models.BooleanField(default=True) # state value if true the file is in use else it is not being used
    comment = models.ForeignKey("comment", on_delete=models.SET_NULL, blank=True, null=True)
    file_extension = models.CharField(max_length=6, null=True, blank=True)
    file_type = models.CharField(max_length = 6,blank=True, null=True)
class comment_react(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    comment = models.ForeignKey("comment", on_delete=models.CASCADE)
    type = models.CharField(max_length=10, default = "like") # could be (like) this for future upgrades to the reaction between the user and the comment
class category(models.Model):
    name = models.CharField(max_length=15)
class group(models.Model):
    creator = models.ForeignKey("user", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    creation_date = models.DateTimeField()
    description = models.TextField()
    is_public = models.BooleanField()
    # moderators = models.TextField(blank=True) # can have a list of user ids who are moderators and default value would be the creator only
    state = models.CharField(max_length=10) # state (working, stopped, suspended) ex. if the creator deleted his account the group will be in stop state
    users_num = models.IntegerField(blank=True) # number of users on the group
class page(models.Model):
    creator = models.ForeignKey("user", on_delete=models.SET_NULL, null=True)
    page_name = models.CharField(max_length=30)
    state = models.CharField(max_length=10) # state (working, stopped, suspended) ex. if the creator deleted his account the page will be in stop state
    creation_date = models.DateTimeField()
    description = models.TextField()
    # moderators = models.TextField() # can have a list of user ids who are moderators and default value would be the creator only
    category = models.ForeignKey("category", on_delete=models.SET_NULL, null=True)
    users_num = models.IntegerField() # number of the users who follow the page
class post_page(models.Model):
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    page = models.ForeignKey("page", on_delete=models.CASCADE)

class post_group(models.Model):
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    group = models.ForeignKey("group", on_delete=models.CASCADE)

# class group_user(models.Model):
#     user = models.ForeignKey("user", on_delete=models.CASCADE)
#     group = models.ForeignKey("group", on_delete=models.CASCADE)

# class post_user(models.Model):
#     user = models.ForeignKey("user", on_delete=models.CASCADE)
#     page = models.ForeignKey("page", on_delete=models.CASCADE)
# # chat section

class thread(models.Model):
    subject = models.CharField(max_length=70)
    thread_creator = models.ForeignKey("user", on_delete=models.SET_NULL, null=True)
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True)
    delete_date = models.DateTimeField(blank=True)
    #encrypted_key = models.CharField(max_length=50, blank=True)
    seed = models.CharField(max_length=10)
    type = models.CharField(max_length=80) # could be (direct, group)
    def get_particpants(self):
        particpants = particpant.objects.filter(thread=self)
        return particpants
    def get_messages(self):
        messages = message.objects.filter(thread=self)
        return messages
class particpant(models.Model):
    thread = models.ForeignKey("thread", on_delete=models.CASCADE)
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    delete_date = models.DateTimeField(null=True, blank=True)
    last_read = models.DateTimeField(blank=True)
    is_active = models.BooleanField(blank=True)

class message_type(models.Model): # types can be video, text, file, picture, collection
    type = models.CharField(max_length=20)
class message(models.Model):
    sender = models.ForeignKey("particpant", on_delete=models.SET_NULL, null=True)
    thread = models.ForeignKey("thread", on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField()
    delete_date = models.DateTimeField()
    last_read = models.DateTimeField()
    is_read = models.BooleanField() # if all the thread particpants readed the message is read
    readers = models.CharField(max_length=100, null=True)
    message_type = models.ForeignKey("message_type", on_delete=models.SET_NULL, null=True)

# admins, reports, levels

class admin_level(models.Model):
    level = models.CharField(max_length=10) # can be in a certain range of levels
    abilities = models.TextField() # list of actions from the admin_actions

class admin_actions(models.Model): # actions that the admin can do
    name = models.CharField(max_length=40)
class admin(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    delete_date = models.DateTimeField()
    admin_level = models.ForeignKey("admin_level", on_delete=models.CASCADE)
    password_hash = models.CharField(max_length=72)

class user_admin(models.Model):
    user = models.ForeignKey("user", on_delete=models.DO_NOTHING) # maybe bad for the integrity of the data
    admin = models.ForeignKey("admin", on_delete=models.PROTECT)
    content = models.TextField()
    reason = models.TextField()
    action = models.ForeignKey("admin_actions", on_delete=models.DO_NOTHING)
    action_date = models.DateTimeField()

# user relations
class friendship(models.Model):
    sender = models.ForeignKey("user", on_delete=models.CASCADE,blank=True, related_name="sender_id")
    receiver = models.ForeignKey("user", on_delete=models.CASCADE,blank=True, related_name="receiver_id")
    state = models.CharField(max_length=10) # can be (pending, accepted, refused)
    send_date = models.DateTimeField()
    creation_date = models.DateTimeField(null=True)
    # creating a follow instance maybe in a function here
class follow(models.Model):
    follower = models.ForeignKey("user", on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey("user", on_delete=models.CASCADE, related_name="followed")


class block(models.Model):
    blocker = models.ForeignKey("user", on_delete=models.CASCADE, related_name="blocker")
    blocked = models.ForeignKey("user", on_delete=models.CASCADE, related_name="blocked")
    creation_date = models.DateTimeField(null=True, default=None)

class user_page(models.Model):
    page = models.ForeignKey("page", on_delete=models.CASCADE)
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    state = models.CharField(max_length=12) # can be (moderator, normal)
    create_date = models.DateTimeField()

class user_group(models.Model):
    group = models.ForeignKey("group", on_delete=models.CASCADE)
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    user_state = models.CharField(max_length=12) # can be (refused, pending, accepted)
    state = models.CharField(max_length=12) # can be (moderator, normal)
    create_date = models.DateTimeField()


class comment_reply(models.Model): # maybe can do this one later
    replied_to = models.ForeignKey("comment", on_delete=models.SET_NULL, null=True, related_name="replied_to")
    replyer = models.ForeignKey("comment", on_delete=models.CASCADE, related_name="replyer")


# this is for authentication

# from django.db.models.fields import IntegerField
# from time import mktime
# class DateTimeIntegerField(IntegerField):

#     def get_prep_value(self, value):
#         if isinstance(value, date):
#             value = mktime(value.timetuple())
#         return super().get_prep_value(value)

#     def to_python(self, value):
#         if isinstance(value, date):
#             value = mktime(value.timetuple())
#         return super().to_python(value)
