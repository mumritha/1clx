from django.core.exceptions import ValidationError
from django import forms
from shop.models import Reg,Log
import re

def validate_name(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Name should not contain digits.")
    if not re.match(r'^[a-zA-Z]+$', value):
        raise ValidationError("Name should contain only letters.")


def validate_email(value):
    if not value:
        raise ValidationError("Email is required.")
    if not re.match("[a-z0-9_\-\.]+[@][a-z]+[\.][a-z]{2,3}", value):
        raise ValidationError("Invalid email address.")
    
def validate_mobilenumber(value):
    if not value:
        raise ValidationError("Mobile number is required.")    
    if not re.match("[0-9]{10}", value):
        raise ValidationError("Invalid mobile number.")
    
def validate_password(value):   
    if not value:
        raise ValidationError("Password is required.")
    if len(value) < 8 or len(value) > 16:
        raise ValidationError("Password length must be between 8 and 16  characters.")
    if not re.search("[a-z]", value):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search("[A-Z]", value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search("[0-9]", value):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r"[@#$%^&+=]", value):
        raise ValidationError("Password must contain at least one special character.")
    if re.search(r"\s", value):
        raise ValidationError("Password must not contain any whitespace characters.")
    


def validate_conformpassword(value):   
    if not value:
        raise ValidationError("Password is required.")
    if len(value) < 8 or len(value) > 16:
        raise ValidationError("Password length must be between 8 and 16  characters.")
    if not re.search("[a-z]", value):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search("[A-Z]", value):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search("[0-9]", value):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r"[@#$%^&+=]", value):
        raise ValidationError("Password must contain at least one special character.")
    if re.search("\s", value):
        raise ValidationError("Password must contain at least one whitespace character.")



class registerForm(forms.Form):
    name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control col-12 col-sm-8 col-md-7', 'rows': 3, 'cols': 40, 'onblur': 'makeSlug(this.value)'}),validators=[validate_name])
    email=forms.EmailField()
    mobilenumber=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class': 'form-control col-12 col-sm-8 col-md-7', 'rows': 3, 'cols': 40, 'onblur': 'makeSlug(this.value)'}),validators=[validate_mobilenumber])
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control col-12 col-sm-8 col-md-7', 'rows': 3, 'cols': 40, 'onblur': 'makeSlug(this.value)'}),validators=[validate_password])
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control col-12 col-sm-8 col-md-7', 'rows': 3, 'cols': 40, 'onblur': 'makeSlug(this.value)'}),validators=[validate_conformpassword])
    
class loginForm(forms.Form):
    email=forms.EmailField(validators=[validate_email])
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control col-12 col-sm-8 col-md-7', 'rows': 3, 'cols': 40, 'onblur': 'makeSlug(this.value)'}))
    
