from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name ="testing"
urlpatterns = [
    path("post/create_comment", views.posts.as_view(), name="create_comment"),
    path("ajaxtest", views.ajax_test, name = "ajaxtest"),
    path("ajax", views.ajax, name="ajax"),
    path("javascript", views.javascriptrender, name="javascriptrender"),
    path("create_post", views.posts.create_post, name="createpost"),
    path("create_postg", views.posts.create_postg, name="createpostg"),
    path("post/<int:post_id>", views.posts.as_view(), name="displaypost"),
    
]   
