from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.urls import reverse
from django.views import generic
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib import messages

from teams.models import Team,TeamMember
from tasks.models import Task,TaskTeam
from teams.forms import AddMemberForm

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

# Method to update related models
def updateDependentModels(member,team):
    TeamMember.objects.create(member=member,team=team)
    for task in member.tasks.all():
        TaskTeam.objects.get_or_create(task=task,team=team)

class CreateTeam(LoginRequiredMixin,generic.CreateView):
    model = Team
    fields = ('name','description')

    def form_valid(self,form):
        form.instance.creator = self.request.user
        form.save()
        member = self.request.user
        team = form.instance
        try:
            updateDependentModels(member,team)
        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(self.request.user.members.team.name)))
        else:
            messages.success(self.request,"You are now a member of the {} group.".format(self.request.user.members.team.name))
        return super(CreateTeam, self).form_valid(form)



class SingleTeam(LoginRequiredMixin,generic.DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super(SingleTeam, self).get_context_data(**kwargs)
        context['add_member_form'] = AddMemberForm
        return context

#add member
class AddMember(LoginRequiredMixin,generic.edit.FormView):
    form_class = AddMemberForm
    template_name = "test.html"

    def form_valid(self,form):
        member = get_object_or_404(User,username=form.cleaned_data["username"])
        team = get_object_or_404(Team,creator=self.request.user)
        try:
            updateDependentModels(member,team)
        except IntegrityError:
            memberteam = TeamMember.objects.filter(member=member)[0].team
            messages.warning(self.request,("{} is already a member of {}".format(member,memberteam)))
        else:
            messages.success(self.request,"{} is now a member of the {} group.".format(member,team))

        self.success_url = reverse('teams:single',kwargs={'slug':team.slug})
        return super(AddMember, self).form_valid(form)
