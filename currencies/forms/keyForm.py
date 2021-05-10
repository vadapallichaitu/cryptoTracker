from ..models import KeyFormModel
from django import forms
from django.contrib.auth.models import User
class KeyForm(forms.ModelForm):
    primary_key = forms.CharField(required=True)
    secret_key = forms.CharField(required=True,widget = forms.PasswordInput)
    
    class Meta:
        model = KeyFormModel
        fields = ("primary_key","secret_key")
