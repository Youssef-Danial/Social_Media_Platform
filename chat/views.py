from django.shortcuts import render
from autheno.cipher_auth import get_user, is_user_auth
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from chat.chat import *
# Create your views here.
def chatt(request):
    if (is_user_auth):
        # getting the user profile
        userinstance = get_user(request)
        data = {
            "profile": userinstance.profile,
            "user":userinstance,
        }
        return render(request, "main/chat.html", data)
    return HttpResponse(reverse_lazy("autheno:login-register"))
def direct_message(request):
    if (is_user_auth(request)):
        # now sending the friend request
        if request.method == 'POST':
            # now receiving the post data
            userinstance = get_user(request)
            data = {
            "profile": userinstance.profile,
            "user":userinstance,
            }
            user_id = request.POST["user"]
            create_direct_thread(request, user_id, type = "direct")
            print(user_id)
        return render(request, "main/chat.html", data)
    return HttpResponse(reverse_lazy("autheno:login-register"))