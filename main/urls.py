from django.urls import path
from django.views.generic import TemplateView
from . import views
app_name = "main"
urlpatterns = [
     path("profile/<int:id>", TemplateView.as_view(template_name="main/profile"), name="profile"),
]