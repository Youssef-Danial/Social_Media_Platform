from django.shortcuts import render
from autheno.cipher_auth import get_user 
# Create your views here.
def chatt(request):
    # getting the user profile
    userinstance = get_user(request)
    data = {
        "profile": userinstance.profile,
        "user":userinstance,
    }
    return render(request, "main/chat.html", data)