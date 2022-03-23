from autheno.cipher_auth import get_user, get_user_profile, get_userbyid, get_pagebyid, get_groupbyid, get_current_datetime
from database.models import friendship, follow, block, page, group, user_page, user_group
import datetime
from django.utils import timezone
from django.db.models import Q
# empty commit
# getting current Time
currentDateTime = datetime.datetime.now(tz=timezone.utc)

def send_friend_request(request, user_id):
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

def is_user_in_group(request, group_id):
    userinstance = get_user(request)
    groupinstance = get_groupbyid(group_id)
    user_group_instance = user_group.objects.filter(group= groupinstance, user= userinstance).first()
    if user_group_instance is not None:
        if user_group_instance.user_state == "accepted":
            return True
        else:
            return False # user state is refused or pending
    else:
        return False

def is_user_follow_page(request, page_id):
    userinstance = get_user(request)
    pageinstance = get_pagebyid(page_id)
    user_page_instance = user_page.objects.filter(page = pageinstance, user= userinstance).first()
    if user_page_instance is not None:
        return True
    else:
        return False


def follow_page(request, page_id):
    try:
        follower = get_user(request)
        pageinstance = get_pagebyid(page_id)
        # now creating a relation with with the follower and the page
        user_page_follow_instance = user_page(page = pageinstance, user = follower, state = "normal", create_date=get_current_datetime())
        user_page_follow_instance.save()
        return True
    except:
        return False
def unfollow_page(request, page_id):
    try:
        follower = get_user(request)
        pageinstance = get_pagebyid(page_id)
        # now creating a relation with with the follower and the page
        user_page_follow_instance = user_page.objects.filter(page = pageinstance, user = follower).first()
        # checking if the user a moderator
        if user_page_follow_instance.state == "moderator":
            return False
        else:
            # deleting the user from the page
            user_page_follow_instance.delete()
        return True
    except:
        return False # the user is not in the page
    
# if the user trying to join a group we should check if the group is public or private 
# if public he joins the group without any problem 
# if private he just send a request that will be shown to the moderators of the group
# and then they can accept or refuse the request
def join_group(request, group_id):
    try:
        follower = get_user(request)
        groupinstance = get_groupbyid(group_id)
        # checking the privacy state of the group
        if groupinstance.is_public and (not is_user_refused_group(request, group_id)): # true mean public false mean private
            # now creating a relation with with the follower and the page
            user_group_follow_instance = user_group(group = groupinstance, user = follower, state = "normal",user_state = "accepted", create_date=get_current_datetime())
            user_group_follow_instance.save()
            return True # joined successfully
        else:
            user_group_follow_instance = user_group(group = groupinstance, user = follower, state = "normal",user_state = "pending", create_date=get_current_datetime())
            user_group_follow_instance.save() 
            return True 
    except:
        return False
    

def leave_group(request, group_id):
    try:
        follower = get_user(request)
        groupinstance = get_groupbyid(group_id)
        # now creating a relation with with the follower and the page
        user_group_follow_instance = user_page.objects.filter(page = groupinstance, user = follower).first()
        # checking if the user a moderator
        if user_group_follow_instance.state == "moderator" or user_group_follow_instance.user_state == "refused":
            return False # the user is a moderator or a refused from the page
        else:
            # deleting the user from the page
            user_group_follow_instance.delete()
            return True
    except:
        return False # user is not in the group

def is_userpage_moderator(request, page_id):
    try:
        userinstance = get_user(request),
        pageinstance = get_pagebyid(page_id)
        user_page_instance = user_page.objects.filter(user=userinstance, page=pageinstance).first()
        if user_page_instance.state == "moderator":
            return True 
        else:
            return False
    except:
        return False # the user is not in the group

def is_usergroup_moderator(request, group_id):
    try:
        userinstance = get_user(request)
        groupinstance = get_groupbyid(group_id)
        user_group_instance = user_group.objects.fitler(user = userinstance, group=groupinstance).first()
        if user_group_instance.state == "moderator":
            return True 
        else:
            return False
    except:
        return False # the user is not in the group

def is_page_creator(request, page_id):
    try:
        userinstance = get_user(request)
        pageinstance = get_pagebyid(page_id)
        if pageinstance.creator == userinstance:
            return True
        else:
            return False
    except:
        return False # something wrong happened in teh page instnace
def is_group_creator(request, group_id):
    try:
        userinstance = get_user(request)
        groupinstance = get_groupbyid(group_id)
        if groupinstance.creator == userinstance:
            return True
        else:
            return False
    except:
        return False

def is_user_refused_group(request, group_id):
    try:
        userinstance = get_user(request)
        groupinstance = get_groupbyid(group_id)
        user_group_instance = user_group.objects.filter(user = userinstance, group = groupinstance).first()
        if user_group_instance.user_state == "refused":
            return True
        else:
            return False
    except:
        return False # the user is not in the group

def get_user_group_join_state(request, group_id):
    try:
        userinstance = get_user(request)
        groupinstance = get_groupbyid(group_id)
        user_group_instance = user_group.objects.filter(user = userinstance, group = groupinstance).first()
        return user_group_instance.user_state
    except:
        return None # the user is not in the group

