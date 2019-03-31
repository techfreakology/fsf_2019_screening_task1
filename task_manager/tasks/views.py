from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.urls import reverse,reverse_lazy
from django.views import generic
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib import messages
from tasks.forms import AssignTaskForm
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

# Create your views here.
from tasks.models import Task,TaskAssignees,TaskTeam

class TaskList(LoginRequiredMixin,generic.ListView):
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

class TaskDetail(LoginRequiredMixin,generic.DetailView):
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
            TaskAssignees.objects.create(task=form.instance,user=self.request.user)
        return super(CreateTask, self).form_valid(form)

class SingleTask(LoginRequiredMixin,generic.DetailView):
    model = Task

class AssignTask(LoginRequiredMixin,generic.edit.FormView):
    form_class = AssignTaskForm
    template_name = "tasks/assign_task_form.html"

    def form_valid(self,form):
        task = get_object_or_404(Task,slug=slugify(form.cleaned_data["task"]))
        user = get_object_or_404(User,username=form.cleaned_data["username"])
        try:
            if user.members and user.members.team == self.request.user.members.team:
                TaskAssignees.objects.create(
                    task = task,
                    user = user
                )
            elif self.request.user != task.creator:
                messages.warning(self.request,("you are not authorized to assign this task, contact {}".format(task.creator)))

        except IntegrityError:
            messages.warning(self.request,("{} is already assigned {}".format(user,task)))
        except AttributeError:
            TaskAssignees.objects.create(
                task = task,
                user = user
            )
            messages.warning(self.request,("{} is not in your team".format(user)))
        self.success_url = reverse_lazy("tasks:single",kwargs={'slug':task.slug})
        return super(AssignTask, self).form_valid(form)
