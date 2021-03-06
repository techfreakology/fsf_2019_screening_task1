from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse,reverse_lazy
from django.views import generic
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib import messages
from tasks.forms import AssignTaskForm,CommentForm
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

# Create your views here.
from tasks.models import Task,TaskAssignees,TaskTeam,Comment

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

    def get_context_data(self, **kwargs):
        context = super(TaskDetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm
        context['assign_task_form'] = AssignTaskForm
        return context

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

class UpdateTask(LoginRequiredMixin,generic.edit.UpdateView):
    model = Task
    fields = ("title","description","status")
    template_name_suffix = '_update_form'

class SingleTask(LoginRequiredMixin,generic.DetailView):
    model = Task


class AssignTask(LoginRequiredMixin,generic.edit.FormView):
    form_class = AssignTaskForm
    template_name = "test.html"

    def get_success_url(self, **kwargs):
        return reverse_lazy('tasks:single',kwargs={'slug':self.kwargs['slug']})

    def form_valid(self,form):
        try:
            user = User.objects.get(username=form.cleaned_data["username"])
            task = get_object_or_404(Task,slug=self.kwargs["slug"])
            if user.members and user.members.team == self.request.user.members.team:
                TaskAssignees.objects.create(
                    task = task,
                    user = user
                )
            elif self.request.user != task.creator:
                messages.warning(self.request,("you are not authorized to assign this task, contact {}".format(task.creator)))
            elif self.requset.user.members.team != user.request.members.team:
                messages.warning(self.request,("{} is not in your team".format(user)))

        except IntegrityError:
            messages.warning(self.request,("{} is already assigned {}".format(user,task)))
        except AttributeError:
            messages.warning(self.request,("{} is not in your team".format(user)))
        except ObjectDoesNotExist:
            messages.warning(self.request,("user does not exists"))

        return super(AssignTask, self).form_valid(form)

class CreateComment(LoginRequiredMixin,generic.edit.FormView):
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('tasks:single',kwargs={'slug':self.kwargs['slug']})

    def form_valid(self, form):
        task = get_object_or_404(Task,slug=self.kwargs["slug"])
        user = get_object_or_404(User,username=self.kwargs["username"])
        message = form.cleaned_data["message"]

        try:
            if user.members and user.members.team == task.creator.members.team:
                Comment.objects.create(
                    task = task,
                    user = user,
                    message = message
                )
            elif self.request.user != task.creator:
                messages.warning(self.request,("you are not authorized to comment on this task, contact {}".format(task.creator)))

        except IntegrityError:
            messages.warning(self.request,("This comment already exists on {} by {}".format(task.title,user)))
        except AttributeError:
            if task.creator == user:
                Comment.objects.get_or_create(
                    task = task,
                    user = user,
                    message = message
                )
            else:
                messages.warning(self.request,("you are not authorized to comment on this task, contact {}".format(task.creator)))
        return super(CreateComment,self).form_valid(form)
