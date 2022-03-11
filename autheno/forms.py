from django.forms import CharField, DateInput, EmailField, ModelForm,PasswordInput, DateField
from database.models import user
from django import forms
from database.models import user
import re
from django.contrib.auth.hashers import make_password, check_password
import datetime

class register(forms.ModelForm):

    user_name = CharField(required=True, min_length=3, max_length=50)
    first_name = CharField(required=True, min_length=3, max_length=50)
    middle_name = CharField(required=True, min_length=3, max_length=50)
    last_name = CharField(required=True, min_length=3, max_length=50)
    password = CharField(required=True, min_length=8,max_length=50,label="Password", widget=forms.PasswordInput)
    passwordconfirm = CharField(required=True, min_length=8,max_length=50, label="Confirm Password", widget=forms.PasswordInput)
    email = EmailField(required=True, min_length=3, max_length=250)
    birthdate= DateField(widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = user
        fields = ['user_name', "first_name", "middle_name", "last_name", "email", "phone_number", "birthdate"]
        labels={
            "user_name": "User Name",
            "first_name": "First Name",
            "middle_name": "Middle Name",
            "last_name": "Last Name",
            "email":"Email Address",
            "birthdate": "Birth Date",
            "phone_number": "Phone Number",

        }



    def clean_user_name(self):
        data = self.cleaned_data["user_name"]
        if re.match(r"^([ \u00c0-\u01ffa-zA-Z'\-])+$", data):
            pass
        else:
            raise forms.ValidationError("Wrong username")
        # checking if there user with the same username in the database
        u = user.objects.filter(user_name=data).first()
        if u == None:
            pass
        else:
            raise forms.ValidationError("This username already Taken")
        return data
    def clean_email(self):
        data = self.cleaned_data["email"]
        if re.match(r"(?:^|\s)[\w!#$%&'*+/=?^`{|}~-](\.?[\w!#$%&'*+/=?^`{|}~-]+)*@\w+[.-]?\w*\.[a-zA-Z]{2,3}\b", data):
            pass
        else:
            raise forms.ValidationError("Wrong Email Address")
        
        # checking if the email already in the database
        u = user.objects.filter(email=data).first()
        if u == None:
            pass
        else:
            raise forms.ValidationError("This Email is already used")
        return data

    def clean_birthdate(self):
        data = self.cleaned_data["birthdate"]
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year =int(date.strftime("%Y")) - int(data.strftime("%Y"))
        if year>14:
            pass
        else:
            raise forms.ValidationError(
                "You are younger than 14 When you get older come"
            )
        return data

    def clean(self):
        cleaned_data = super(register, self).clean()
        # first checking if the password matchs
        password = cleaned_data["password"]
        passwordcon = cleaned_data["passwordconfirm"]
        if password != passwordcon:
            raise forms.ValidationError(
                "password and confirm password does not match"
            )
        # checking the password if it is match the requirements
        if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", password):
            pass
        else:
            raise forms.ValidationError("Wrong Password")
        return cleaned_data     

class login_u(forms.Form):
    email = EmailField()
    password = CharField(widget=PasswordInput)
