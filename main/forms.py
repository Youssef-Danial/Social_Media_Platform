from django import forms
from database.models import post
class post(forms.ModelForm):

    class Meta:
        model = post
        fields = [""]

