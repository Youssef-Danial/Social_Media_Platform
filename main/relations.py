from autheno.cipher_auth import get_user, get_user_profile, get_userbyid
from database.models import friendship, follow, block, page, group
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
    try:
        friendrequest = friendship.objects.filter(sender = sender, receiver = receiver).frist()
        friendrequest.creation_date = currentDateTime
        friendrequest.state = "accepted"
        # sending the friend request by saving it to the database
        friendrequest.save()
    except:
        return False
    return True

def reject_friendrequest(request, user_id):
    receiver = get_user(request)
    sender = get_userbyid(user_id)
    try:
        friendrequest = friendship.objects.filter(sender = sender, receiver = receiver).frist()
        friendrequest.state = "refused"
    except:
        return False
    return True

def follow_user(request,user_id):
    follower = get_user(request)
    followed = get_userbyid(user_id)
    try:
        followinstance = follow(follower = follower, followed=followed)
        followinstance.save()
    # to be continue to check if the user blocked this user before or not before sending the friend request or being refused more than 3 times
    except:
        return False
    return True

def block_user(request, user_id):
    blocker = get_user(request)
    blocked = get_userbyid(user_id)
    try:
        blockinstance = block(blocker =blocker, blocked=blocked, creation_date=currentDateTime)
        blockinstance.save()
    except:
        return False
    return True
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
    friendinstance = friendship.objects.filter(Q(sender = user) | Q(receiver = user), state="accepted").values()
    if friendinstance != None:
        return friendinstance
    else:
        return None

def get_mutualfriends(request, user_id):
    # declaring an empty list for the mutual friends
    mutualfriendslist = []
    # getting the users
    user1  = get_user(request)
    #user2 = get_userbyid(user_id)
    user1_friends = get_friendlist(user1.id)
    user2_friends = get_friendlist(user_id)
    # checking if the there is a similar friends between the two users
    for user in user1_friends:
        if user in user2_friends:
            mutualfriendslist.append(user)
    if len(mutualfriendslist) > 0: # checking if there is mutual friends in the list
        return mutualfriendslist
    else:
        return False # there is no mutual friends 
    

def get_followers(user_id):
    # checking the followers of the userid
    user = get_userbyid(user_id)
    followinstance = follow.objects.filter(followed = user).values()
    # checking if the user have followers
    if len(followinstance) > 0:
        return followinstance
    else:
        return False # there is no users following the given user
def get_blocks(request):
    # getting user by request
    user = get_user(request)
    # checking the users that this user have blocked
    blockinstance = block.objects.filter(blocker = user).values()
    if len(blockinstance) > 0:
        return blockinstance
    else:
        return False # the user is not blocking anyone

def get_follows(request):
    # getting the user
    user = get_user(request)
    followinstance = follow.objects.filter(follower = user).values()
    if len(followinstance)>0:
        return followinstance
    else:
        return False # there is no one this user follows

def get_friendrequests(request):
    # getting user
    user = get_user(request)
    friendrequestlist = friendship.objects.filter(sender = user, state = "pending").values()
    if len(friendrequestlist)>0:
        return friendrequestlist
    else:
        return False # there is not pending friend request for this user



def follow_page(request, page):
    pass

def unfollow_page(request, page):
    pass

def join_group(request, group):
    pass

def leave_group(request, group):
    pass

def is_userpage_moderator(request, page):
    pass

def is_usergroup_moderator(request, group):
    pass

def is_page_creator(request, page):
    pass

def is_group_creator(request, group):
    pass

def is_user_refused_group(request, group):
    pass
