from database.models import page, group, user_group, user_page, file
from autheno.cipher_auth import is_user_auth, get_current_datetime, get_pagebyid, get_user, get_userbyid, get_groupbyid
from main.relations import is_page_creator, is_group_creator, is_usergroup_moderator
from main.notifications import create_notification

# notifications (groupaccept, grouprefuse, groupremove, adminadd, adminremove) # do not forget to add groupremove, adminadd, adminremove
def create_page(request, data):
    try:
        if is_user_auth(request):
            creator = data["creator"]
            page_name = data["page_name"]
            state = data["state"]
            creation_date = get_current_datetime()
            description = data["description"]
            category = data["category"]
            page_instance = page(creator = creator, page_name = page_name, state = state, creation_date = creation_date, description = description, category = category)
            page_instance.save()
            # page created successfully
            return True
        else:
            return False
    except:
        return False

def create_groupfunc(request, data):
    #try:
        if is_user_auth(request):
            creator = data["creator"]
            name = data["name"]
            creation_date = get_current_datetime()
            state = data["state"]
            is_public = data["is_public"]
            description = data["description"]
            grouppfp = file.objects.get(pk=10)
            group_instance = group(grouppfp = grouppfp,creator = creator, name = name, state = state, creation_date = creation_date, description = description, is_public = is_public, users_num = 1)
            group_instance.save()
            # group created successfully
            return True
        else:
            return False
    #except:
        #return False

def delete_page(request, page_id):
    try:
        if is_user_auth(request):
            # now we check if the user is the creator
            if is_page_creator(request):
                # now if the user is the page creator we can delete it
                page_instance = get_pagebyid(page_id)
                page_instance.delete()
                # page have been deleted successfully
                return True
        else:
            return False
    except:
        return False

def delete_group(request, group_id):
    try:
        if is_user_auth(request):
            if is_group_creator(request):
                # is the user is the group creator he can delete it
                group_instance = get_groupbyid(group_id)
                group_instance.delete()
                return True
        else:
            return False
    except:
        return False

def get_group_requests(request, group_id):
    #try:
        if is_user_auth(request):
            # if is_group_creator(request) or is_usergroup_moderator(request, group_id):
                # making sure that the information only appears for creator or moderator of the group
                group_instance = get_groupbyid(group_id)
                user_group_instances = user_group.objects.filter(group=group_instance, user_state = "pending")
                return user_group_instances
            # else:
            #     return None
        else:
            return None
    #except:
        #return None

def get_group_users(request, group_id):
    #try:
        if is_user_auth(request):
            #if is_group_creator(request) or is_usergroup_moderator(request, group_id):
                # making sure that the information only appears for creator or moderator of the group
                group_instance = get_groupbyid(group_id)
                user_group_instances = user_group.objects.filter(group=group_instance, user_state = "accepted")
                return user_group_instances
            #else:
                #return None
        else:
            return None

def accept_group_request(user_id, group_id):
    #try:
        # getting the user and the group_id
        follower = get_userbyid(user_id)
        groupinstance = get_groupbyid(group_id)
        create_date = get_current_datetime()
        user_group_follow_instance = user_group(group = groupinstance, user = follower, state = "normal",user_state = "accepted", create_date = create_date)
        groupinstance.users_num = int(groupinstance.users_num) + 1
        user_group_follow_instance.save()
        return True
    #except:
        return False


def accept_group_request_done(user_id, group_id):
    #try:
        # getting the user and the group_id
        follower = get_userbyid(user_id)
        groupinstance = get_groupbyid(group_id)
        user_group_follow_instance = user_group.objects.filter(group = groupinstance, user = follower).first()
        groupinstance.users_num = int(groupinstance.users_num) + 1
        user_group_follow_instance.user_state = "accepted"
        user_group_follow_instance.save()
        return True
    #except:
        return False

def refuse_group_request(user_id, group_id):
    try:
        # getting the user and the group_id
        follower = get_userbyid(user_id)
        groupinstance = get_groupbyid(group_id)
        user_group_follow_instance = user_group.objects.filter(group = groupinstance, user = follower).first()
        groupinstance.users_num = int(groupinstance.users_num) + 1
        user_group_follow_instance.user_state = "refused"
        user_group_follow_instance.save()
        return True
    except:
        return False

def add_user_to_group(request, user_id, group_id, objectinstance):
    #try:
        if is_user_auth(request):
            if is_group_creator(request, group_id) or is_usergroup_moderator(request, group_id):
                if accept_group_request_done(user_id, group_id):
                    # getting the user who accepted the request
                    sender = get_user(request)
                    sender_id = sender.id
                    # now sending notification for the user about the group
                    create_notification(sender_id = sender_id, receipt_id = user_id ,objecttype = objectinstance,source=sender_id, source_name = "user")
                    return True
            else:
                
                return False
        else:
            
            return False
    #except:
        #return False

def refuse_user_from_group(request, user_id, group_id):
    try:
        if is_user_auth(request):
            if is_group_creator(request) or is_usergroup_moderator(request, group_id):
                if refuse_group_request(user_id, group_id):
                    # getting the user who accepted the request
                    sender = get_user(request)
                    sender_id = sender.id
                    # now sending notification for the user about the group
                    #objectinstance = object.objects.filter(name = "grouprefuse").first()
                    create_notification(sender_id = sender_id, receipt_id = user_id ,objecttype = "grouprefuse",source=sender_id, source_name = "user")
                    return True
            else:
                return False
        else:
            return False
    except:
        return False

def is_user_in_groupbyid(user_id, group_id):
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

def remove_user_from_group(request, group_id, user_id):
    try:
        if is_user_auth(request):
            if is_group_creator(request) or is_usergroup_moderator(request, group_id):
                if is_user_in_groupbyid(user_id, group_id) and  refuse_group_request(user_id, group_id):
                    # getting the user who accepted the request
                    sender = get_user(request)
                    sender_id = sender.id
                    groupinstance = get_groupbyid(group_id)
                    groupinstance.users_num = int(groupinstance.users_num) - 1 
                    # now sending notification for the user about the group
                    #objectinstance = object.objects.filter(name = "groupremove").first()
                    create_notification(sender_id = sender_id, receipt_id = user_id ,objecttype = "groupremove",source=sender_id, source_name = "user")
                    return True
            else:
                return False
        else:
            return False
    except:
        return False
def make_user_mod_group(request, user_id, group_id):
    try:
        if is_user_auth(request):
            if is_group_creator(request, group_id):

                    # getting teh user and making him admin
                    user_instance = get_userbyid(user_id)
                    group_instance = get_groupbyid(group_id)
                    user_group_instance = user_group.objects.filter(user=user_instance, group = group_instance).first()
                    user_group_instance.state = "moderator"
                    user_group_instance.save()
                    # getting the user who made the action
                    sender = get_user(request)
                    sender_id = sender.id
                    # now sending notification for the user about the group
                    #objectinstance = object.objects.filter(name = "adminadd").first()
                    create_notification(sender_id = sender_id, receipt_id = user_id ,objecttype = "adminadd",source=sender_id, source_name = "user")
                    return True

        else:
            return False
    except:
        return False

def remove_user_mod_group(request, user_id, group_id):
        try:
            if is_user_auth(request):
                if is_group_creator(request, group_id):
                        # getting teh user and making him admin
                        user_instance = get_userbyid(user_id)
                        group_instance = get_groupbyid(group_id)
                        user_group_instance = user_group.objects.filter(user=user_instance, group = group_instance).first()
                        user_group_instance.state = "normal"
                        user_group_instance.save()
                        # getting the user who made the action
                        sender = get_user(request)
                        sender_id = sender.id
                        # now sending notification for the user about the group
                        #objectinstance = object.objects.filter(name = "adminremove").first()
                        create_notification(sender_id = sender_id, receipt_id = user_id ,objecttype ="adminremove",source=sender_id, source_name = "user")
                        return True
            else:
                return False
        except:
            return False

def make_user_mod_page(request, user_id, group_id):
        try:
            if is_user_auth(request):
                if is_group_creator(request):
                        # getting teh user and making him admin
                        user_instance = get_userbyid(user_id)
                        page_user = get_groupbyid(group_id)
                        user_group_instance = user_group.objects.filter(user=user_instance, group = group_instance).first()
                        user_group_instance.state = "normal"
                        user_group_instance.save()
                        # getting the user who made the action
                        sender = get_user(request)
                        sender_id = sender.id
                        # now sending notification for the user about the group
                        #objectinstance = object.objects.filter(name = "adminremove").first()
                        create_notification(sender_id = sender_id, receipt_id = user_id ,objecttype = "adminremove",source=sender_id, source_name = "user")
                        return True
            else:
                return False
        except:
            return False




def remove_user_mod_page(request, user_id, group_id):
    pass

def edit_page_information(request):
    pass

def edit_group_information(request):
    pass

# try:
#     if is_user_auth(request):
#
#     else:
#         return False
# except:
#     return False
