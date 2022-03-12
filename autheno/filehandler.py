import profile
from django import forms
from database.models import file
import datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import os
from django.core.files import File # for handling files
from autheno.cipher_auth import get_user
# creating the form that will receive the files
class file_receiver(forms.Form):
    file = forms.FileField()


def receive_file(request, state):
    
    if request.method == 'POST':
        # receving the file from the request
        form = file_receiver(request.POST, request.FILES)
        file_ = request.FILES['file']
        if form.is_valid():
            # converting the form to a dictionary
            file_received = form.cleaned_data
            # getting the current time for the uploaded_date for the file
            currentDateTime = datetime.datetime.now(tz=timezone.utc)
            # saving the file
            # getting user
            u = get_user(request)
            folder_path = make_dir(u.id, state = state)
            fs = FileSystemStorage(location=folder_path)
            file_path = os.path.join(folder_path, str(file_))
            filesaver = file(file_name=str(file_path), uploaded_date=currentDateTime)
            fs.save(filesaver.file_name,file_)
            filesaver.save()
            return filesaver
    else:
        form = file_receiver()
        print("waiting for a file")
    return form

def make_dir(user_id, state=None):
    user_id = str(user_id)
    # this line need to be changed every time the website files be moved
    BASE_PATH = "/mnt/d5064e14-3714-48f3-a540-4364ee86b5fe/GP_Workplace/main/gp/src/social/database/files"
    new_path = os.path.join(BASE_PATH, user_id)
    # creating a directory if it does not exist
    try:
        if not os.path.exists(new_path):
            os.mkdir(new_path)
    except:
        pass
    # to store profile files like : (profile picture and background picture)
    if state == "profile":
        profile_path = os.path.join(new_path, "profile")
        try:
            if not os.path.exists(profile_path):
                 os.mkdir(profile_path)
        except:
            pass
        #new_path =  os.path.join("database/files", user_id)
        #profile_path = os.path.join(new_path, "profile")
        return profile_path
    else:
        # to be continue
        return None
    # to be continue

def load_file(file_to_load):
    pass
