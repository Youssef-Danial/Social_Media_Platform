from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name ="testing"
urlpatterns = [
    path("ajaxtest", views.ajax_test, name = "ajaxtest"),
    path("ajax", views.ajax, name="ajax"),
    path("javascript", views.javascriptrender, name="javascriptrender"),
    path("create_post", views.post, name="createpost"),
]   
