from django import template
from autheno.cipher_auth import *
from database.models import post_react, block, comment_react, user_group, group

register = template.Library()


@register.simple_tag
def is_user_reacted_post(user_id, post_id): # to check if the user reacted or not to the post so he could not react again
    # getting  the user and the post
    try:
        userinstance = get_userbyid(user_id)
        postinstance = get_postbyid(post_id)
        post_react_instance = post_react.objects.filter(user_id = userinstance, post_id = postinstance).first() # the default is set for like for now
        
        if post_react_instance != None:
            return True # mean the user reacted to the post
        else:
            return False # the user did not react to the post
    except:
        return False # there something wrong with the user or the post maybe the do not exist


@register.simple_tag
def is_user_reacted_comment(user_id, comment_id): # to check if the user reacted or not to the post so he could not react again
    # getting  the user and the post
    try:
        userinstance = get_userbyid(user_id)
        commentinstance = get_commentbyid(comment_id)
        comment_react_instance = comment_react.objects.filter(user = userinstance, comment = commentinstance).first() # the default is set for like for now
        
        if comment_react_instance != None:
            return True # mean the user reacted to the post
        else:
            return False # the user did not react to the post
    except:
        return False # there something wrong with the user or the post maybe the do not exist


@register.simple_tag
def test_tag():
    return 12

@register.simple_tag
def is_post_owner(user_id, post_id):
    try:
        # checking if the user is the owner of the post
        userinstance = get_userbyid(user_id)
        post_instance = get_postbyid(post_id)
        if post_instance.user == userinstance:
            return True
        else:
            return False
    except:
        return False


@register.simple_tag
def is_blockr(blocker_id, blocked_id):
    blocker = get_userbyid(blocker_id)
    blocked = get_userbyid(blocked_id)
    blockinstance = block.objects.filter(blocker=blocker, blocked=blocked).first()
    # print(f"the result--------{blockinstance}")
    if blockinstance != None:
        return True
    else:
        return False

@register.simple_tag
def is_comment_owner(user_id, comment_id):
    try:
        userinstance = get_userbyid(user_id)
        # postinstance = get_postbyid(post_id)
        commentinstance = get_commentbyid(comment_id)
        if commentinstance.user == userinstance:
            return True
        else:
            return False
    except:
        return False

@register.simple_tag
def is_message_owner(message, user_id):
    try:
        user_instance = get_userbyid(user_id)
        if message.sender == user_instance:
            return True
        return False
    except:
        return False

@register.simple_tag
def is_group_CorM(userid,groupid): # checking if the user is moderator or creator of the page
    try:
        userinstance = get_userbyid(userid)
        groupinstance = get_groupbyid(groupid)
        user_group_instance = user_group.objects.fitler(user = userinstance, group=groupinstance).first()
        if user_group_instance.state == "moderator" or groupinstance.creator == userinstance:
            return True
        else:
            return False
    except:
        return False # the user is not in the group

@register.simple_tag
def is_group_creator(userid, groupid):
    try:
        userinstance = get_user(userid)
        groupinstance = get_groupbyid(groupid)
        if groupinstance.creator == userinstance:
            return True
        else:
            return False
    except:
        return False

   