from pyexpat import model
from django.db import models
from sqlalchemy import null

# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=12)
    email = models.EmailField(max_length=70)
    password_hash = models.CharField(max_length=72)
    phone_number = models.CharField(max_length=50)
    birthdate = models.DateField()

class profile(models.Model):
    about_me = models.TextField(max_length=100)
    pic_url = models.CharField(max_length=100)
    backpic_url = models.CharField(max_length=100)
    link = models.URLField()
    user = models.ForeignKey("user", on_delete=models.CASCADE)


class activity_type(models.Model):
    activity_name = models.CharField(max_length=20)

class object_type(models.Model):
    object_name = models.CharField(max_length=20)
    object_url = models.URLField()
class notification(models.Model):
    receipt_id = models.ForeignKey("user", on_delete=models.SET_NULL, null = True)
    sender_id = models.ForeignKey("user", on_delete=models.SET_NULL, null = True)
    activity_type = models.ForeignKey("activity_type", on_delete=models.SET_NULL, null = True)
    object_type = models.CharField("object_type", on_delete=models.SET_NULL, null = True)
    time_sent = models.DateTimeField()
    time_read = models.DateTimeField()
    is_read = models.BooleanField()

class setting_code(models.Model):
    setting_name = models.CharField(max_length=50)
    default_value = models.CharField(max_length=20)

class user_settings(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    setting_code = models.ForeignKey("setting_code")
    value = models.CharField(max_length=20)
    modify_date = models.DateTimeField()

class post(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    date = models.DateTimeField()
    text_content = models.TextField()
    pictures = models.TextField(null=True)
    video = models.ForeignKey("video", on_delete=models.SET_NULL, null=True)
    who_can_see = models.TextField()
    interaction_counter = models.CharField()
    post_state = models.IntegerField()

class comment(models.Model):
    user = models.ForeignKey("user", on_delete=models.CASCADE)
    post = models.ForeignKey("post", on_delete=models.CASCADE)
    content = models.TextField()
    attach_url = models.TextField()
    date = models.DateTimeField()
    interaction_counter = models.CharField()

class category(models.Model):
    name = models.CharField()
class group(models.Model):
    user = models.ForeignKey("user", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    creation_date = models.DateTimeField()
    description = models.TextField()
    is_public = models.BooleanField()
    moderators = models.TextField() # can have a list of user ids who are moderators and default value would be the creator only
    state = models.CharField() # state (working, stopped, suspended) ex. if the creator deleted his account the group will be in stop state
    users_num = models.IntegerField() # number of users on the group
class page(models.Model):
    user = models.ForeignKey("user", on_delete=models.SET_NULL, null=True)
    state = models.CharField() # state (working, stopped, suspended) ex. if the creator deleted his account the page will be in stop state
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
    subject = models.CharField()
    creation_date = models.DateTimeField()
    update_date = models.DateTimeField()
    delete_date = models.DateTimeField()
    encrypted_key = models.CharField()
    seed = models.CharField()

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
    sender = models.ForeignKey("particpant", on_delete=models.CASCADE)
    thread = models.ForeignKey("thread", on_delete=models.CASCADE)
    content = models.TextField()
    creation_date = models.DateTimeField()
    delete_date = models.DateTimeField()
    last_read = models.DateTimeField()
    is_read = models.BooleanField() # if all the thread particpants readed the message is read
    readers = models.CharField(null=True)
    message_type = models.ForeignKey("message_type", on_delete=models.SET_NULL, null=True)

# admins, reports, levels

class admin_level(models.Model):
    level = models.CharField() # can be in a certain range of levels
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
    sender = models.ForeignKey("user", on_delete=models.CASCADE)
    receiver = models.ForeignKey("user", on_delete=models.CASCADE)
    state = models.CharField() # can be (pending, accepted, refused)
    send_date = models.DateTimeField()
    creation_date = models.DateTimeField(null=True) 

class follow(models.Model):
    follower = models.ForeignKey("user", on_delete=models.CASCADE)
    followed = models.ForeignKey("user", on_delete=models.CASCADE)


class block(models.Model):
    blocker = models.ForeignKey("user", on_delete=models.CASCADE)
    blocked = models.ForeignKey("user", on_delete=models.CASCADE)
    stopped_date = models.DateTimeField(null=True) # can be null 