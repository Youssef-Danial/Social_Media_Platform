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
     
     
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)