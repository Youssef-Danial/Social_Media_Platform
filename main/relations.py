from autheno.cipher_auth import get_user, get_user_profile, get_userbyid
from database.models import friendship, follow, block
import datetime
from django.utils import timezone

# getting current Time
currentDateTime = datetime.datetime.now(tz=timezone.utc)

def friend_request(request, user_id):
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    friendrequest = friendship(sender = sender, receiver = receiver, state="pending", send_date=currentDateTime, created_at=None)
    # sending the friend request by saving it to the database
    friendrequest.save()
    # to be continue to check if the user blocked this user before or not before sending the friend request or being refused more than 3 times

def accept_friendrequest(request, user_id):
    receiver = get_user(request)
    sender = get_userbyid(user_id)
    friendrequest = friendship.objects.filter(sender = sender, receiver = receiver).frist()
    friendrequest.creation_date = currentDateTime
    friendrequest.state = "accepted"
    # sending the friend request by saving it to the database
    friendrequest.save()

def reject_friendrequest(request, user_id):
    receiver = get_user(request)
    sender = get_userbyid(user_id)
    friendrequest = friendship.objects.filter(sender = sender, receiver = receiver).frist()
    friendrequest.state = "refused"

def follow_user(request,user_id):
    follower = get_user(request)
    followed = get_userbyid(user_id)
    followinstance = follow(follower = follower, followed=followed)
    followinstance.save()
    # to be continue to check if the user blocked this user before or not before sending the friend request or being refused more than 3 times

def block_user(request, user_id):
    blocker = get_user(request)
    blocked = get_userbyid(user_id)
    blockinstance = block(blocker =blocker, blocked=blocked)
    blockinstance.save()

def is_friend(request, user_id):
    receiver = get_user(request)
    sender = get_userbyid(user_id)
    friendinstance = friendship.objects.filter(sender = sender, receiver=receiver).first()
    if friendinstance != None:
        return True
    else:
        return False

def is_follower(request, user_id):
    follower = get_user(request)
    followed = get_userbyid(user_id)
    followinstance = follow.objects.filter(follower = follower, followed=followed).first()
    if followinstance != None:
        return True
    else:
        return False
def is_followed(request, user_id):
    followed = get_user(request)
    follower = get_userbyid(user_id)
    followinstance = follow.objects.filter(follower = follower, followed=followed).first()
    if followinstance != None:
        return True
    else:
        return False
def is_blocked(request, user_id):
    blocked = get_user(request)
    blocker = get_userbyid(user_id)
    blockinstance = block.objects.filter(blocker=blocker, blocked=blocked)
    if blockinstance != None:
        return True
    else:
        return False
def is_blocker(request, user_id):
    blocker = get_user(request)
    blocked = get_userbyid(user_id)
    blockinstance = block.objects.filter(blocker=blocker, blocked=blocked)
    if blockinstance != None:
        return True
    else:
        return False