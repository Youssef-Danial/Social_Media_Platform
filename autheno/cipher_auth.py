from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import datetime
from django.utils import timezone
from database.models import particpant, user, profile, page, group, user_group, user_page, post, comment, notification, thread
# cipher authentication part
def auth_user(request, user_email, password):
    # adding a email to the session
    
    u = user.objects.filter(email=user_email).first()
    if u != None:
        if check_password(password, u.password_hash):
            request.session["email"] = user_email
            # updating the last login
            
            u.last_login = get_current_datetime()
            u.save()
            request.session["last_login"] = str(u.last_login)
        else:
            messages.error(request, "Password does not match")
    else:
        messages.error(request, "User does not exist in the system")

def is_user_auth(request):
    # checking if the request sessions have the auth credientials
    if "email" in request.session:
        return True
    else:
        return False

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

# this function check if the session user is equal to another user
def user_equal(request, u):
    # getting the user who is on the session right now
    u_own = get_user(request)
    if u_own.id == u.id:
        return True
    else:
        return False
def get_user_profile(u):
    p = profile.objects.get(user = u)
    return p


def get_current_datetime():
    currentDateTime = datetime.datetime.now(tz=timezone.utc)
    return currentDateTime


def get_groupbyid(group_id):
    try:
        groupinstance = group.objects.get(pk=group_id)
        return groupinstance
    except:
        return None
def get_pagebyid(page_id):
    try:
        pageinstance = page.objects.get(pk=page_id)
        return pageinstance
    except:
        return None


def get_group_by_creator(request):
    try:
        creator = get_user(request)
        grouplist = group.objects.filter(creator = creator).values()
        return grouplist
    except:
        return None

def get_page_by_creator(request):
    try:
        creator = get_user(request)
        pagelist = page.objects.filter(creator = creator).values()
        return pagelist
    except:
        return None

def get_postbyid(post_id):
    try:
        postinstance = post.objects.get(pk=post_id)
        return postinstance
    except:
        return None

def get_commentbyid(comment_id):
    try:
        commentinstance = comment.objects.get(pk=comment_id)
        return commentinstance
    except:
        return None

def get_notificationbyid(notification_id):
    try:
        notification_instance = notification.objects.get(pk=notification_id)
        return notification_instance
    except:
        return None
def get_threadbyid(thread_id):
    try:
        thread_instance = thread.objects.get(pk=thread_id)
        return thread_instance
    except:
        return None
    
def get_particpantbyid(participant_id):
    try:
        particpant_instance = particpant.objects.get(pk=participant_id)
        return particpant_instance
    except:
        return None

def is_user_auth_and_verified():
    pass

def get_verfied():
    pass

def send_verification_message():
    pass
