from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from autheno.cipher_auth import get_postbyid, is_user_auth, get_user
from autheno.filehandler import receive_files
from database.models import profile, post_group
from main.post_comment import *
from django.forms import Form
from django.views import View
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from main.relations import *
# Create your views here.
def ajax_test(request):
    profileinstance = profile.objects.get(pk=1)
    aboutme = profileinstance.about_me
    return JsonResponse({"aboutme": aboutme})  
def ajax(request):
    return render(request, "testing/ajaxtest.html")  

def javascriptrender(request):
    return render(request, "testing/javascript.html")


def get_user_last_post(request):
    userinstance = get_user(request)
    postinstance = post.objects.filter(user=userinstance).last()
    return postinstance

def get_user_last_comment(request):
    userinstance = get_user(request)
    commentinstance = comment.objects.filter(user=userinstance).last()
    return commentinstance
# def create_post(postinstance):
#     postobject = f"""<div class="post-container">
#         <div class="post-row">
#           <div class="user-profile">
#             <a href="/main/profile/{postinstance.user.id}"> <img class="pfppic" src="/static{postinstance.user.profile.pfp.file_url}" alt="profile picture"></a>
#               <div>
#                  <p>{postinstance.user.user_name}</p>
#                  <span>{postinstance.who_can_see}</span>
#                  <span>{postinstance.get_timeago}</span>
#               </div>      
#           </div>
#     </div>
#           <p class="post-text"><b>    let fly into space</b></p>    
#               <img src="/static/files/2/post/1LQq.gif" alt="post picture" style="width:100%">
#       <hr>
#         <div class="post-row">
#            <div class="activity-icons">
#              <div id="post53">
#                <button class="like" id="like53" value="53" style="padding: 0;border: none;background: none;font-size: 20px;"> <span id="like53span" class="bi bi-hand-thumbs-up-fill" style="color:None"></span></button><p id="num53">1</p></div>
#              <div><img src="/static/images/profile/comments.png"> 0</div>
#            </div>
#         </div>
#      </div>"""
class posts(View):
    def get(self, request, post_id):
        userinstance = get_user(request)
        postinstance = load_post(request, post_id)
        # and (not is_blocked(request, postinstance.user.id))
        if is_user_auth(request):
            data = {
                "post": postinstance,
                "is_owner": False,
                "user": userinstance,
                "viewer":userinstance.id,
            }
            # checking if the user is permetted to see the post

            if is_post_owner(request, post_id):
                # should display edit and delete button
                data["is_owner"] = True
            # else it should display the post data

            return render(request,"main/display_post.html",data)
        else:
            return HttpResponse("You are not authenticated try loging in or you can not view this post") 
   

    def create_post(request):
        if is_user_auth(request):
            fileslist = receive_files(request, state="post")
            if request.method == "POST":
                # getting user data
                request.POST._mutable = True
                u = get_user(request)
                data = request.POST
                data["instance_name"] = u.user_name
                data["instance_id"] = u.id
                if create_post(request, data,fileslist):
                    postinstance = get_user_last_post(request)
                    rendered = render_to_string('main/post.html', { 'post': postinstance,"viewer":u.id })
                    response = {"newpost":rendered}
                    if data["post_location"] == "group":
                        groupinstance = get_groupbyid(data["groupidd"])
                        postgroupinstance = post_group(postinstance,groupinstance)
                        postgroupinstance.save()
                    return JsonResponse(response,status=200)
                    # return HttpResponse("success")
                else:
                    return HttpResponse("User is not authenticated")
            return render(request, "testing/post.html",{"form":fileslist})
        return HttpResponse("User is not authenticated try to login")

    def create_postg(request):
        if is_user_auth(request):
            fileslist = receive_files(request, state="post")
            if request.method == "POST":
                # getting user data
                print("inside the group create post")
                request.POST._mutable = True
                u = get_user(request)
                data = request.POST
                print(request.POST)
                for i in data.items():
                    print(i)
                print("====================")
                data["who_can_see"] = "public"
                data["instance_name"] = u.user_name
                data["instance_id"] = u.id
                if create_post(request, data,fileslist):
                    postinstance = get_user_last_post(request)
                    rendered = render_to_string('main/post.html', { 'post': postinstance,"viewer":u.id })
                    response = {"newpost":rendered}
                    if data["post_location"] == "group":
                        groupinstance = get_groupbyid(data["groupidd"])
                        postgroupinstance = post_group(post = postinstance,group = groupinstance)
                        postgroupinstance.save()
                    return JsonResponse(response,status=200)
                    # return HttpResponse("success")
                else:
                    return HttpResponse("User is not authenticated")
            return render(request, "testing/post.html",{"form":fileslist})
        return HttpResponse("User is not authenticated try to login")
    # def disply_edit_post(request, post_id):
    #     if is_user_auth(request):
    #         if is_post_owner(request, post_id):
    #             # now he can edit the post
    #             # getting the post 
    #             postinstance = get_postbyid(post_id)
    #             data={
    #                 "post":postinstance
    #             }
    #             return render(request, "testing/editpost.html", data)
    # def editpost(request, post_id):
    #     if is_user_auth(request):
    #         if is_post_owner(request, post_id):
    #             # now he can edit the post
    #             data = request.POST
    #             edit_post()
    #             return render(request, "testing/editpost.html", data)


    # def post(self,request, post_id):
    #     print("create comment called ==========================----=-=-=-=-")
    #     print(is_user_auth(request))
    #     print("create comment called ==========================----=-=-=-=-")
    #     if is_user_auth(request):
    #         print("the function is called")
    #         fileslist = receive_files(request, state="comment")
    #         if request.method == "POST":
    #             # getting user data
    #             request.POST._mutable = True
    #             u = get_user(request)
    #             data = request.POST
    #             data["user"] = u
    #             if create_comment(request, data,fileslist):
    #                 HttpResponseRedirect(reverse("testing:displaypost", args=[int(data["post"])]))
    #             else:
    #                 return HttpResponse("User is not authenticated")
    #         print("file should show up")
    #         return HttpResponseRedirect(reverse("testing:displaypost", args=[post_id]))
    #     return HttpResponse("User is not authenticated try to login")

    def post(self,request):
        print("create comment called ==========================----=-=-=-=-")
        print(is_user_auth(request))
        print("create comment called ==========================----=-=-=-=-")
        if is_user_auth(request):
            print("the function is called")
            fileslist = receive_files(request, state="comment")
            if request.method == "POST":
                # getting user data
                request.POST._mutable = True
                u = get_user(request)
                data = request.POST
                data["user"] = u
                if create_comment(request, data,fileslist):
                    commentinstance = get_user_last_comment(request)
                    rendered = render_to_string('main/comment.html', { 'comment': commentinstance,"viewer":u.id })
                    response = {"newcomment":rendered}
                    return JsonResponse(response,status=200)
                else:
                    return HttpResponse("User is not authenticated")
            print("file should show up")
            return HttpResponseRedirect(reverse("testing:displaypost", args=[int(data["post"])]))
        return HttpResponse("User is not authenticated try to login")