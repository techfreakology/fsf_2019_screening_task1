from django import forms
from django.contrib.auth.models import User
from tasks.models import Task
from django.utils.text import slugify


class AssignTaskForm(forms.Form):
    username = forms.CharField()


class CommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
