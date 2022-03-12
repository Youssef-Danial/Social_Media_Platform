from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "main"
urlpatterns = [
     path("profile/<int:user_id>", views.profile.as_view(), name="profile"),
     path("profile/edit", views.profile.edit_pfp, name="edit_pfp"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)