from django import template
from autheno.cipher_auth import *
from database.models import post_react, block, comment_react, user_group, group

register = template.Library()



@register.simple_tag
def is_group_CorM(userid,groupid): # checking if the user is moderator or creator of the page
    try:
        userinstance = get_userbyid(userid)
        groupinstance = get_groupbyid(groupid)
        user_group_instance = user_group.objects.filter(user = userinstance, group=groupinstance).first()
        if  groupinstance.creator == userinstance: 
            return True
        elif user_group_instance != None and user_group_instance.state == "moderator":
            return True
        else:
            return False
    except:
       return False # the user is not in the group



@register.simple_tag
def isgroupcreator(userid, groupid):
    try:
        userinstance = get_userbyid(userid)
        groupinstance = get_groupbyid(groupid)
        if groupinstance.creator == userinstance:
            return True
        else:
            return False
    except:
        return False



@register.simple_tag
def is_user_member(user_id, group_id):
    userinstance = get_userbyid(user_id)
    groupinstance = get_groupbyid(group_id)
    user_group_instance = user_group.objects.filter(group= groupinstance, user= userinstance).first()
    if user_group_instance is not None:
        if user_group_instance.user_state == "accepted":
            return True
        else:
            return False # user state is refused or pending
    else:
        return False



@register.simple_tag
def is_user_requesting(user_id, group_id):
        # making sure that the information only appears for creator or moderator of the group
        group_instance = get_groupbyid(group_id)
        userinstance = get_userbyid(user_id)
        user_group_instance = user_group.objects.filter(group=group_instance, user = userinstance, user_state = "pending").first()
        if user_group_instance is not None:
            return True
        else:
            return False



@register.simple_tag
def get_userid_by_email(email):
    userinstance = user.objects.filter(email=email).first()
    return userinstance.id