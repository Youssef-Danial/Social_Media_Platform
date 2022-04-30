from django import template
from autheno.cipher_auth import *
from database.models import post_react

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
