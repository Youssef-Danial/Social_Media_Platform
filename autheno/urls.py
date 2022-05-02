from django.urls import path
from django.views.generic import TemplateView
from . import views
app_name = "autheno"
urlpatterns = [
    path("registerd", views.registery.register,name="register"),
    path("logind", views.login.login , name="login"),
    #path("home", TemplateView.as_view(template_name = "authenticate/home.html"), name="home"),
    path("home", views.home, name="home"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("login-register",views.login_register, name="login-register"),
    path("logout", views.logout, name="logout"),
    path("register", views.registere,name="registere"),
    path("login", views.logine , name="logine"),
]