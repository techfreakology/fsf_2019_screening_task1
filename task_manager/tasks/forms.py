from django import forms
from django.contrib.auth.models import User
from tasks.models import Task
from django.utils.text import slugify

class AssignTaskForm(forms.Form):
    task = forms.CharField()
    username = forms.CharField()

    def clean(self):
        if(not Task.objects.filter(slug=slugify(self.cleaned_data["task"])).exists()):
            raise forms.ValidationError("Please enter exact Task Title")
        if(not User.objects.filter(username=self.cleaned_data["username"]).exists()):
            raise forms.ValidationError("Please enter correct username")
        return self.cleaned_data
