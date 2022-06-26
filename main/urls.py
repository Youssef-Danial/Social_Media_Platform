from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "main"
urlpatterns = [
     path("profile/<int:user_id>", views.profile.as_view(), name="profile"),
     path("profile/edit_pfp", views.profile.edit_pfp, name="edit_pfp"),
     path("profile/edit_backpfp", views.profile.edit_backpfp, name="edit_backpfp"),
     path("proifle/edit_about", views.profile.edit_about_me, name="edit_about_me"),
     path("add", views.add_friend, name="add-friend"),
     path("unfriend", views.un_friend, name="un-friend"),
     path("notifications", views.show_notifications, name="notifications"),
     path("notif_markread", views.notif_markread, name="notif_markread"),
     path("follow", views.follow_friend, name="follow-friend"),
     path("unfollow", views.unfollow_friend, name="unfollow-friend"),
     path("acceptfriend", views.accept_friend , name="accept-friend"),
     path("rejectfriend", views.reject_friend , name="reject-friend"),
     path("like_post", views.like_post, name="like_post"),
     path("remove_like_post", views.remove_like_post, name="remove_like_post"),
     path("settings", views.show_settings, name="settings"),
     path("change_email", views.change_email, name="change_email"),
     path("change_username", views.change_username, name="change_username"),
     path("change_phonenumber", views.change_phonenumber, name="change_phonenumber"),
     path("change_password", views.change_password, name="change_password"),
     path("remove_post", views.remove_post, name="remove-post"),
     path("block_friend", views.block_friend, name="block-friend"),
     path("unblock_friend", views.unblock_friend, name="unblock-friend"),
     path("remove_comment", views.remove_comment, name="remove-comment"),
     path("like_comment", views.like_comment, name="like_comment"),
     path("remove_like_comment", views.remove_like_comment, name="remove_like_comment"),
     path("new_comments", views.new_comments,name="new_comments"),
     path("is_there_notifications", views.is_there_notifications, name="is_there_notifications"),
     path("search/", views.get_search, name="search"),
     path("friends/",views.friends ,name="friends"),
     path("group/<int:group_id>", views.groupe.as_view(), name="group"),
     path("create_group", views.create_group, name="create_group"),
     path("group_settings/<int:group_id>", views.group_settings.as_view(), name="group_settings"),
     path("create_group_request", views.create_group_request, name = "create_group_request"),
     path("accept_group_request",views.accept_group_request,name="accept_group_request"),
     path("remove_user_group", views.remove_user_group,name="remove_user_group"),
     path("remove_group_request", views.remove_group_request,name="remove_group_request"),
     path("refuse_group_request", views.refuse_group_requestt, name="refuse_group_request"),
     path("remove_group_requestban", views.remove_group_requestban, name="remove_group_requestban"),
     path("make_mod", views.make_mod, name="make_mod"),
     path("remove_mod", views.remove_mod, name="remove_mod"),
     path("change_group_pfp/<int:group_id>", views.change_group_pfp.as_view(), name="change_group_pfp"),
     path("deletegroup",views.delete_groupp, name="deletegroup"),
     path("edit_group_desc", views.edit_group_desc, name="edit_group_desc"),

     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)