from django import forms
from django.contrib.auth.models import User
from tasks.models import Task
from django.utils.text import slugify


class AssignTaskForm(forms.Form):
    username = forms.CharField()

    def clean(self):
        if(not User.objects.filter(username=self.cleaned_data["username"]).exists()):
            raise forms.ValidationError("Please enter correct username")
        return self.cleaned_data

class CommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
