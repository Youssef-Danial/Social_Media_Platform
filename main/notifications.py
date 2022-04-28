from autheno.cipher_auth import get_current_datetime, get_userbyid, get_notificationbyid
from database.models import notification, object

def create_object(name, text): # this is for admins
    try:
        objectinstance = object(name=name, text=text)
        objectinstance.save()
        return True
    except:
        return False

def create_notification(sender_id, receipt_id, objecttype, source=None):
    try:
        # creating notification
        time_sent = get_current_datetime()
        sender = get_userbyid(sender_id)
        receipt = get_userbyid(receipt_id)
        object_type = object.objects.filter(object_type = objecttype)
        # creating a notification instance
        notification_instance = notification(senderr = sender, receipt = receipt, object_type = object_type, time_sent=time_sent, source=source)
        notification_instance.save()
        return True
    except:
        return False

def make_notification_read(request, notification_id):
    try:
        time_read = get_current_datetime()
        notification_instance = get_notificationbyid(notification_id)
        notification_instance.time_read = time_read
        notification_instance.is_read = True
        notification_instance.save()
        return True
    except:
        return False

def get_user_notifications(request, state="unread"):
    try:
        userinstance = get_userbyid(request)
        # now searching and getting all the notifications that have been sent to this user
        if state =="unread":
            notifications = notification.objects.filter(receipt = userinstance, is_read = False).order_by("-time_sent")
            return notifications
        elif state == "read":
            notifications = notification.objects.filter(receipt = userinstance, is_read = True).order_by("-time_sent")
            return notifications
        else: # this mean all the notifications
            notifications = notification.objects.filter(receipt = userinstance).order_by('-time_sent')
            return notifications
    except:
        return None

# name = "commentpost"
# text = "commented on you post"
# create_object(name, text)
# name = "commentcomment"
# text = "replied to you"
# create_object(name, text)
# name = "follow"
# text = "followed you"
# create_object(name, text)
# name = "friendrequest"
# text = "sent you a friend request"
# create_object(name, text)
# name = "message"
# text = "sent you a message"
# create_object(name, text)
# name = "block"
# text = "blocked you"
# create_object(name, text)
