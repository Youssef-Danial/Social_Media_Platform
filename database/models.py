from pyexpat import model
from django.db import models
from sqlalchemy import null
import datetime
from django.utils import timezone
currentDateTime = datetime.datetime.now(tz=timezone.utc)
# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=12)
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



class activity_type(models.Model):
    activity_name = models.CharField(max_length=20)

class object_type(models.Model):
    object_name = models.CharField(max_length=20)
    object_url = models.URLField()
class notification(models.Model):
    receipt_id = models.ForeignKey("user", on_delete=models.SET_NULL, null = True, related_name="receipt")
    sender_id = models.ForeignKey("user", on_delete=models.SET_NULL, null = True, related_name="sender")
    activity_type = models.ForeignKey("activity_type", on_delete=models.SET_NULL, null = True)
    object_type = models.ForeignKey("object_type", on_delete=models.SET_NULL, null = True)
    time_sent = models.DateTimeField()
    time_read = models.DateTimeField()
    is_read = models.BooleanField()

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
    who_can_see = models.TextField() # can be (followers, onlyme)
    interaction_counter = models.CharField(max_length=50) # this should be dictionary of keys(reactiontype): values(number of reaction)
    # post_state = models.IntegerField() #
    post_location = models.CharField(max_length=7) # this should be (profile, page, group)
    def get_files(self):
        return postfile.objects.filter(post=self).values()
    postfiles=property(get_files)
class postfile(models.Model):
    file_name = models.CharField(max_length=250)
    uploaded_date = models.DateTimeField()
    file_url = models.CharField(max_length=250)
    is_used = models.BooleanField(default=True) # state value if true the file is in use else it is not being used
    post = models.ForeignKey("post", on_delete=models.SET_NULL, blank=True, null=True)
    file_extension = models.CharField(max_length=6, null=True, blank=True)
# class video(models.Model):
#     name=models.CharField(max_length=50)
#     video_url = models.TextField()
#     state = models.CharField(max_length=10) # have a state censored or deleted
#     is_used = models.BooleanField(default=True) # state value if true the file is in use else it is not being used
class comment(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    content = models.TextField()
    attach_url = models.ForeignKey("file",on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField()
    interaction_counter = models.CharField(max_length=50)

class category(models.Model):
    name = models.CharField(max_length=15)
class group(models.Model):
    user = models.ForeignKey("user", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField()
    description = models.TextField()
    is_public = models.BooleanField()
    moderators = models.TextField() # can have a list of user ids who are moderators and default value would be the creator only
    state = models.CharField(max_length=10) # state (working, stopped, suspended) ex. if the creator deleted his account the group will be in stop state
    users_num = models.IntegerField() # number of users on the group
class page(models.Model):
    user = models.ForeignKey("user", on_delete=models.SET_NULL, null=True)
    state = models.CharField(max_length=10) # state (working, stopped, suspended) ex. if the creator deleted his account the page will be in stop state
    creation_date = models.DateTimeField()
    description = models.TextField()
    moderators = models.TextField() # can have a list of user ids who are moderators and default value would be the creator only
    category = models.ForeignKey("category", on_delete=models.SET_NULL, null=True)
    users_num = models.IntegerField() # number of the users who follow the page
class post_page(models.Model):
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    page = models.ForeignKey("page", on_delete=models.CASCADE)

class post_group(models.Model):
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    group = models.ForeignKey("group", on_delete=models.CASCADE)

class group_user(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    group = models.ForeignKey("group", on_delete=models.CASCADE)

class post_user(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    page = models.ForeignKey("page", on_delete=models.CASCADE)
# chat section

class thread(models.Model):
    subject = models.CharField(max_length=70)
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()
    delete_date = models.DateTimeField()
    encrypted_key = models.CharField(max_length=50)
    seed = models.CharField(max_length=10)

class particpant(models.Model):
    thread = models.ForeignKey("thread", on_delete=models.CASCADE)
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    creation_date = models.DateTimeField()
    delete_date = models.DateTimeField()
    last_read = models.DateTimeField()
    is_active = models.BooleanField()

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
    sender = models.ForeignKey("user", on_delete=models.CASCADE, related_name="sender_id")
    receiver = models.ForeignKey("user", on_delete=models.CASCADE, related_name="receiver_id")
    state = models.CharField(max_length=10) # can be (pending, accepted, refused)
    send_date = models.DateTimeField()
    creation_date = models.DateTimeField(null=True)

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
    user_state = models.CharField(max_length=12) # can be (moderator, normal)
    state = models.CharField(max_length=12) # can be (refused, accepted)
    create_date = models.DateTimeField()
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