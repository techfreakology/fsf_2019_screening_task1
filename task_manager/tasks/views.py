from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.urls import reverse
from django.views import generic
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
from tasks.models import Task,TaskAssignees,TaskTeam

class TaskList(generic.ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_team = None
        try:
            if self.request.user.members.team:
                task_team = TaskTeam.objects.filter(
                    team = self.request.user.members.team
                )
        except User.DoesNotExist:
            raise Http404
        except AttributeError:
            pass
        else:
            context["task_team"] = task_team
        return context

class TaskDetail(generic.DetailView):
    model = Task

class CreateTask(LoginRequiredMixin,generic.CreateView):
    model = Task
    fields = ('title','description','status')

    def form_valid(self,form):
        form.instance.creator = self.request.user
        form.save()
        try:
            if self.request.user.members.team:
                TaskTeam.objects.get_or_create(
                    team = self.request.user.members.team,
                    task = form.instance
                )
        except AttributeError:
            TaskAssignees.objects.create(task=form.instance,assignee=self.request.user)
        return super(CreateTask, self).form_valid(form)

class SingleTask(generic.DetailView):
    model = Task
