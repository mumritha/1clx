from django.core.exceptions import ValidationError
from django import forms
from shop.models import Product
import re



def validate_name(value):
    if any(char.isdigit() for char in value):
        raise ValidationError("Name should not contain digits.")
    if not re.match(r'^[a-zA-Z]+$', value):
        raise ValidationError("Name should contain only letters.")
    

def validate_slug(value):
    if value is None or len(value) == 0:
        raise ValidationError("Slug cannot be empty.")
    if any(char.isdigit() for char in value):
        raise ValidationError("Slug should not contain digits.")
    if any(char.isspace() for char in value):
        raise ValidationError("Slug should not contain spaces.")
    if any(char.isupper() for char in value):
        raise ValidationError("Slug should not contain uppercase letters.")
    if not re.match(r'^[a-z-]+$', value):
        raise ValidationError("Slug should not contain special characters other than hyphen (-) and should be in lowercase.")





def validate_description(value):
    if len(value) < 20:
        raise ValidationError("Description should be at least 20 characters.")
def validate_short_description(value):
    if len(value) < 20:
        raise ValidationError("Short Description should be at least 20 characters.") 

def validate_image(value):
    if value is None or len(value) == 0:
        return None
    
 

def validate_price(value):
    if value < 0:
        raise ValidationError("Price must be greater than 0")

def validate_tax(value):
    if value < 0 or value > 100:
        raise ValidationError("Tax value must be between 0 and 100.")
def validate_discount(value):
    if value < 0 or value > 100:
        raise ValidationError("Discount value must be between 0 and 100.")    
    
class editProductForm(forms.Form):
  
    name = forms.CharField(validators=[validate_name])
    unit = forms.ChoiceField(choices=[('', 'Select unit'), (1, 'Qty'), (2, 'Ltr'), (3, 'ML'), (4, 'KG'), (5, 'GM'), (6, 'Meter')])
    slug = forms.CharField(validators=[validate_slug]) 
    description = forms.CharField(validators=[validate_description],widget=forms.Textarea(attrs={'class': 'form-control col-12 col-sm-8 col-md-7', 'rows': 3, 'cols': 40, 'onblur': 'makeSlug(this.value)'}))
    short_description = forms.CharField(validators=[validate_short_description],widget=forms.Textarea(attrs={'class': 'form-control col-12 col-sm-8 col-md-7', 'rows': 3, 'cols': 40, 'onblur': 'makeSlug(this.value)'}))
    image1= forms.ImageField(required=False,validators=[validate_image])
    alt1= forms.CharField()
    image2= forms.ImageField(required=False,validators=[validate_image])
    alt2= forms.CharField()
    image3= forms.ImageField(required=False,validators=[validate_image])
    alt3= forms.CharField()
    price = forms.IntegerField(validators=[validate_price])
    discount = forms.IntegerField(validators=[validate_discount])
    tax = forms.IntegerField(validators=[validate_tax])
    Stock = forms.ChoiceField(choices=[(1, 'in_stock'), (2, 'out_of_stock')], widget=forms.RadioSelect(), initial=0)
    stockqty = forms.IntegerField()
    visibility = forms.ChoiceField(choices=[(1, 'published'), (2, ' hidden')], widget=forms.RadioSelect(), initial=0) 
    publish_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-100 border-1 border p-1 text-secondary mt-2'}))

    














   
   



     