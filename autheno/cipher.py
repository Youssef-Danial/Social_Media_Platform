from django.contrib.auth.hashers import make_password, check_password
from database.models import user
from django.contrib import messages
import datetime
from django.utils import timezone
# cipher authentication part
def auth_user(request, user_email, password):
    # adding a email to the session
    
    u = user.objects.filter(email=user_email).first()
    if u != None:
        if check_password(password, u.password_hash):
            request.session["email"] = user_email
            # updating the last login
            currentDateTime = datetime.datetime.now(tz=timezone.utc)
            date = currentDateTime
            u.last_login = date
            u.save()
            request.session["last_login"] = str(u.last_login)
        else:
            messages.error(request, "Password does not match")
    else:
        messages.error(request, "User does not exist in the system")

def is_user_auth(request):
    # checking if the request sessions have the auth credientials
    if "email" in request.session:
        return True
    else:
        return False