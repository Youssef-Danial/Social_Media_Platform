from autheno.cipher_auth import get_user, get_user_profile, get_userbyid, get_pagebyid, get_groupbyid, get_current_datetime
from database.models import friendship, follow, block, page, group, user_page, user_group
import datetime
from django.utils import timezone
from django.db.models import Q
from main.notifications import *

# getting current Time


def send_friend_request(request, user_id):
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    currentDateTime = get_current_datetime()
    create_notification(sender.id, receiver.id,'friendrequest', source=sender.id, source_name = "user")
    if sender!= None and receiver != None:
        friendrequest = friendship(sender_id = sender.id, receiver_id = receiver.id, state="pending", send_date=currentDateTime,creation_date = None)
        if is_blocked(request, user_id):
            del friendrequest
            return False
        else : # sending the friend request by saving it to the database
            friendrequest.save()
            return True
    else:
        print(sender)
        print(receiver)
    # to be continue to check if the user blocked this user before or not before sending the friend request or being refused more than 3 times

def accept_friendrequest(request, user_id):
        receiver = get_user(request)
        sender = get_userbyid(user_id)
        currentDateTime = get_current_datetime()
    # try:
        friendrequest = friendship.objects.filter(sender_id = sender, receiver_id = receiver).first()
        print("===================="+str(friendrequest))
        friendrequest.creation_date = currentDateTime
        friendrequest.state = "accepted"
        # sending the friend request by saving it to the database
        friendrequest.save()
        create_notification(receiver.id, sender.id,'friendacccepted', source=receiver.id, source_name = "user")
        print("done==============================")
    # except:
    #     return False
    # return True

def reject_friendrequest(request, user_id):
    receiver = get_user(request)
    sender = get_userbyid(user_id)
    try:
        friendrequest = friendship.objects.filter(sender_id = sender, receiver_id = receiver).first()
        friendrequest.state = "refused"
        friendrequest.save()
        create_notification(receiver.id, sender.id,'friendrefused', source=receiver.id, source_name = "user")
    except:
        return False
    return True

def follow_user(request,user_id):
    # follow notification name
    follower = get_user(request)
    followed = get_userbyid(user_id)
    try:
        followinstance = follow(follower = follower, followed=followed)
        followinstance.save()
        create_notification(follower.id, followed.id,'follow', source=follower.id, source_name = "user")
    # to be continue to check if the user blocked this user before or not before sending the friend request or being refused more than 3 times
    except:
        return False
    return True

def block_user(request, user_id):
    blocker = get_user(request)
    blocked = get_userbyid(user_id)
    currentDateTime = get_current_datetime()
    try:
        blockinstance = block(blocker =blocker, blocked=blocked, creation_date=currentDateTime)
        blockinstance.save()
        # now remove any friend or follow
        unfollow_in(user_id, blocker.id)
    except:
        return False
    return True
def is_friend(request, user_id):
    receiver = get_user(request)
    sender = get_userbyid(user_id)
    friendinstancereceiver = friendship.objects.filter(sender_id = sender, receiver_id=receiver).first()
    friendinstancesender   = friendship.objects.filter(sender_id = receiver, receiver_id=sender).first()
    print(friendinstancereceiver)
    print(friendinstancesender)
    if friendinstancereceiver != None :
        if friendinstancereceiver.state == "accepted" or friendinstancereceiver.state == "accepted" or friendinstancereceiver.state == "pending":
            return True
    elif friendinstancesender != None:
        if friendinstancesender.state == "accepted" or friendinstancesender.state == "accepted" or friendinstancesender.state == "pending":
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
    blockinstance = block.objects.filter(blocker=blocker, blocked=blocked).first()
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

def unfollow_in(user_id1, user_id):
    follower = get_userbyid(user_id1)
    followed = get_userbyid(user_id)
    try:
        # if the user is a follower we remove him from the following
        followerinstance = follow.objects.filter(follower = follower, followed = followed).first()
        followerinstance.delete()
        return True
    except:
        return False # you did not follow the user to unfollow


def unfriend(request, user_id):
    print("friend remove called")
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    if(is_friend(request, user_id)):
        # getting friendship instance and deleting it
        friendinstancesender = friendship.objects.filter(sender_id = sender, receiver_id = receiver).first()
        friendinstancereceiver = friendship.objects.filter(sender_id = receiver, receiver_id = sender).first()
        if friendinstancesender != None:
            friendinstancesender.delete()
            print("true--------- sender")
            # return False
            return True
        if friendinstancereceiver != None:
            friendinstancereceiver.delete()
            print("true---------")
            return True
        else:
            return False
    else:
        return False
def unfriend_request(request, user_id):
    sender = get_user(request)
    receiver = get_userbyid(user_id)
    if(is_friend_requested(request, user_id)):
        # getting friendship instance and deleting it
        friendinstance = friendship.objects.filter(sender_id = sender, receiver_id = receiver)
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
    friendinstance = friendship.objects.filter(Q(sender_id = user) | Q(receiver_id = user), state="accepted")
    if friendinstance != None:
        return friendinstance
    else:
        return friendinstance

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
    if len(mutualfriendslist) >= 1: # checking if there is mutual friends in the list
        return len(mutualfriendslist)

    else:
        return 0 # there is no mutual friends


def get_followers(user_id):
    # checking the followers of the userid
    user = get_userbyid(user_id)
    followinstance = follow.objects.filter(followed = user) 
    # checking if the user have followers
    if len(followinstance) > 0:
        return followinstance
    else:
        return None # there is no users following the given user
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
    followinstance = follow.objects.filter(follower = user)
    if len(followinstance)>0:
        return followinstance
    else:   
        return followinstance # there is no one this user follows

def get_friendrequests(request):
    # getting user
    user = get_user(request)
    friendrequestlist = friendship.objects.filter(sender_id = user, state = "pending").values()
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
        if not is_user_refused_group(request, group_id):
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
        user_group_follow_instance = user_group.objects.filter(group = groupinstance, user = follower).first()
        # checking if the user a moderator
        if user_group_follow_instance.state == "moderator":
            return False # the user is a moderator or a refused from the group
        else:
            # deleting the user from the group
            user_group_follow_instance.delete()
            return True
    except:
        return False # user is not in the group

def unban(user_id, group_id):
    try:
        follower = get_userbyid(user_id)
        groupinstance = get_groupbyid(group_id)
        # now creating a relation with with the follower and the page
        user_group_follow_instance = user_group.objects.filter(group = groupinstance, user = follower).first()
        # checking if the user a moderator
        if user_group_follow_instance.state == "moderator":
            return False # the user is a moderator or a refused from the group
        else:
            # deleting the user from the group
            user_group_follow_instance.delete()
            return True
    except:
        return False # user is not in the group

def leave_groupp(user_id, group_id):
    try:
        follower = get_userbyid(user_id)
        groupinstance = get_groupbyid(group_id)
        # now creating a relation with with the follower and the page
        user_group_follow_instance = user_group.objects.filter(group = groupinstance, user = follower).first()
        # checking if the user a moderator
        if user_group_follow_instance.state == "moderator" or user_group_follow_instance.user_state == "refused":
            return False # the user is a moderator or a refused from the group
        else:
            # deleting the user from the group
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
        user_group_instance = user_group.objects.filter(user = userinstance, group=groupinstance).first()
        if  groupinstance.creator == userinstance: 
            return True
        elif user_group_instance != None and user_group_instance.state == "moderator":
            return True
        else:
            return False
    except:
       return False

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
def is_user_refused_groupbyid(user_id, group_id):
    try:
        userinstance = get_userbyid(user_id)
        groupinstance = get_groupbyid(group_id)
        user_group_instance = user_group.objects.filter(user = userinstance, group = groupinstance).first()
        if user_group_instance.user_state == "refused":
            return True
        else:
            return False
    except:
        return False
def get_user_group_join_state(request, group_id):
    try:
        userinstance = get_user(request)
        groupinstance = get_groupbyid(group_id)
        user_group_instance = user_group.objects.filter(user = userinstance, group = groupinstance).first()
        return user_group_instance.user_state
    except:
        return None # the user is not in the group
