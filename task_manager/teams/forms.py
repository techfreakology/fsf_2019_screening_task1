from django import forms
from django.contrib.auth.models import User

class AddMemberForm(forms.Form):
    username = forms.CharField()
