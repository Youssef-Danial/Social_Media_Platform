from database.models import thread, message, particpant
from autheno.cipher_auth import get_threadbyid, get_particpantbyid, get_user, get_userbyid, is_user_auth, get_current_datetime, get_userbyid
import numpy as np


def create_particpant(user_instance, thread_id):
    #try:
        print("inside")
        user_instance = get_userbyid(user_instance)
        thread_instance = get_threadbyid(thread_id)
        creation_date = get_current_datetime()
        particpant_instance = particpant(thread = thread_instance, user=user_instance, creation_date=creation_date)
        particpant_instance.save()
        print("working")
        # user created successfully
        return True
    #except:
        #return False
def delete_particpant(user_instance, thread_id):
    try:
        thread_instance = get_threadbyid(thread_id)
        particpant_instance = particpant.objects.filter(thread = thread_instance, user=user_instance).first()
        particpant_instance.delete()
        # user created successfully
        return True
    except:
        return False
def leave_thread(request, thread_id):
    try:
        if is_user_auth(request):
            user_instance = get_user(request)
            delete_particpant(user_instance, thread_id)
            return True
        else:
            return False
    except:
        return False
        
def create_thread(request, subject="default", type = "direct"):
    #try:
        if is_user_auth(request):
            print("user is authenticated")
            user_instance = get_user(request)
            if subject =="default":
                subject = user_instance.user_name
            creation_date = get_current_datetime()
            seed = 1234 # generate_seed()
            thread_instance = thread(thread_creator=user_instance,subject = subject,creation_date = creation_date,type = type, seed=seed)
            thread_instance.save()
            print(f"the thread id {thread_instance.id}")
            return thread_instance.id
    #except:
        return None

def there_is_no_thread(request, user_id):
    user_threads = get_user_threads(request)
    other_user = get_userbyid(user_id)
    for threadinstance in user_threads:
        # checking each thread if the user is already a particpant in
        if threadinstance.type == "direct":
            thread_particpants = threadinstance.get_particpants()
            for partic in thread_particpants:
                if partic.user == other_user:             
                    return False
    
    return True
def create_direct_thread(request, user_id, type = "direct"):
    try:
        if is_user_auth(request) and there_is_no_thread(request, user_id):
            thread_id =  create_thread(request)
            owneruser = get_user(request)
            if thread_id != None:
                print("before creating")
                create_particpant(owneruser.id,thread_id)
                create_particpant(user_id, thread_id)
            print("thread have been created successfully=================")
        return True
    except:
        return False


def add_particpant_to_thread(request, user_id, thread_id):
    try:
        if is_user_auth(request):
            user_instance = get_userbyid(user_id)
            create_particpant(user_instance,thread_id)
    except:
        return False

def make_particpant_active(request, thread_id):
    try:
        if is_user_auth(request):
            thread_instance = get_threadbyid(thread_id)
            user_instance = get_user(request)
            particpant_instance = particpant.objects.filter(thread = thread_instance , user=user_instance).first()
            particpant_instance.is_active = True
            particpant_instance.save()
        else:
            return False
    except:
        return False

def make_particpant_inactive(request, thread_id):
    try:
        if is_user_auth(request):
            thread_instance = get_threadbyid(thread_id)
            user_instance = get_user(request)
            particpant_instance = particpant.objects.filter(thread = thread_instance , user=user_instance).first()
            particpant_instance.is_active = False
            particpant_instance.save()
        else:
            return False
    except:
        return False

def get_user_threads(request):
    try:
        if(is_user_auth(request)):
            user_instance = get_user(request)
            particpant_instances = particpant.objects.filter(user = user_instance)
            # getting each thread for each particpant
            thread_list = []
            for particpant_instance in particpant_instances:
                thread_list.append(particpant_instance.thread)
            return thread_list
        else:
            return None
    except:
        return None
        
def generate_encryption_key(request):
    pass

def generate_seed(request):
    data = np.random.randint(100,size=(4))
    return data

def is_particpant_active(request, thread_id):
    try:
        if is_user_auth(request):
            thread_instance = get_threadbyid(thread_id)
            user_instance = get_user(request)
            particpant_instance = particpant.objects.filter(thread = thread_instance , user=user_instance).first()
            if particpant_instance.is_active:
                return True # is active
            else:
                return False # is inactive
        else:
            return False
    except:
        return False
    

def make_user_active(request):
    try:
        if is_user_auth(request):
            thread_list = get_user_threads(request)
            for thread_instance in thread_list:
                make_particpant_active(request, thread_instance.id)
        else:
            return False
    except:
        return False

def is_particpant(request, thread_id):
    try:
        if is_user_auth(request):
            thread_instance = get_threadbyid(thread_id)
            user_threads = get_user_threads(request)
            if thread_instance in user_threads:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def get_particpant(user_id, thread_id):
    try:
        user_instance = get_userbyid(user_id)
        thread_instance = get_threadbyid(thread_id)
        thread_particapnts = thread_instance.get_particapnts()
        for particpant_instance in thread_particapnts:
            if particpant_instance.user == user_instance:
                return particpant_instance
        return None # the user does not exist in the thread 
    except:
        return None
def create_group_thread(request):
    pass

def make_message(user_id, thread_id, data):
    try:
        thread_instance = get_threadbyid(thread_id)
        sender = get_userbyid(user_id)
        creation_date = get_current_datetime()
        message_type = "text"
        message_instance = message(sender = sender, thread=thread_instance, content=data, creation_date=creation_date, message_type=message_type)
        message_instance.save()
        return message_instance
    except:
        return None