from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "chat"
urlpatterns = [
    path("", views.chatt, name="chat"),
    path("messagedirect", views.direct_message, name="messagedirect"),

]