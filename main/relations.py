from autheno.cipher_auth import get_user, get_user_profile, get_userbyid
from database.models import friendship, follow, block
import datetime
from django.utils import timezone
from django.db.models import Q

# getting current Time
currentDateTime = datetime.datetime.now(tz=timezone.utc)

def friend_request(request, user_id):
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    friendrequest = friendship(sender = sender, receiver = receiver, state="pending", send_date=currentDateTime, created_at=None)
    if is_blocked(sender, receiver):
        del friendrequest
        return False
    else : # sending the friend request by saving it to the database
        friendrequest.save()
        return True
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
    blockinstance = block(blocker =blocker, blocked=blocked, creation_date=currentDateTime)
    blockinstance.save()

def is_friend(request, user_id):
    receiver = get_user(request)
    sender = get_userbyid(user_id)
    friendinstancereceiver = friendship.objects.filter(sender = sender, receiver=receiver).first()
    friendinstancesender   = friendship.objects.filter(sender = receiver, receiver=sender).first()
    if friendinstancereceiver != None or friendinstancesender != None:
            if friendinstancesender.state == "accepted" or friendinstancereceiver.state == "accepted":
                return True
    else:
        return False
def is_friend_requested(request, user_id):
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    friendinstance = friendship.objects.filter(sender = sender, receiver=receiver).first()
    if friendinstance != None:
        if friendinstance.state == "pending":
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

def unblock(request, user_id):
    blocker = get_user(request)
    blocked = get_userbyid(user_id)
    # handling errors if the user is not blocked
    if (is_blocker(request,user_id)): # this check if the user is really blocked
        # now we remove the block state
        blockinstance = block.objects.filter(blocker=blocker, blocked=blocked).first()
        blockinstance.delete() # deleting the block instance
        return True
    else:
        return False # you did not block the user to unblock

def unfollow(request, user_id):
    follower = get_user(request)
    followed = get_userbyid(user_id)
    if (is_follower(request,user_id)):
        # if the user is a follower we remove him from the following
        followerinstance = follow.objects.filter(follower = follower, followed = followed).first()
        followerinstance.delete()
        return True
    else:
        return False # you did not follow the user to unfollow

def unfriend(request, user_id):
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    if(is_friend(request, user_id)):
        # getting friendship instance and deleting it
        friendinstancesender = friendship.objects.filter(sender = sender, receiver = receiver).first()
        friendinstancereceiver = friendship.objects.filter(sender = receiver, receiver = sender).first()
        if friendinstancesender != None or friendinstancereceiver != None:
            try:
                friendinstancesender.delete()
                friendinstancereceiver.delete()
            except:
                return False
            return True
        else:
            return False

def unfriend_request(request, user_id):
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    if(is_friend_requested(request, user_id)):
        # getting friendship instance and deleting it
        friendinstance = friendship.objects.filter(sender = sender, receiver = receiver).first()
        if friendinstance != None:
            try:
                friendinstance.delete()
            except:
                return False # the friendship does not exist
            return True # done
        else:
            return False # the friendship does not exist

def get_friendlist(user_id): # this function should return a list of friend objects
    user = get_userbyid(user_id)
    # seraching for the friends of this user
    friendinstance = friendship.objects.filter(Q(sender = user_id) | Q(receiver = user_id)).values()
    if friendinstance != None:
        return friendinstance
    else:
        return None

def get_mutualfriends():    
    pass

def get_followers():
    pass

def get_blocks():
    pass

def get_followinglist():
    pass