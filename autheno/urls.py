from django.urls import path
from django.views.generic import TemplateView
from . import views
app_name = "autheno"
urlpatterns = [
    path("register", views.registery.register,name="register"),
    path("login", views.login.login , name="login"),
    #path("home", TemplateView.as_view(template_name = "authenticate/home.html"), name="home"),
    path("home", views.home, name="home"),
    path("profile/<int:id>", views.profile, name="profile")    
]