from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.urls import reverse
from django.views import generic
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib import messages

from teams.models import Team,TeamMember
from teams.forms import AddMemberForm

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
class CreateTeam(LoginRequiredMixin,generic.CreateView):
    model = Team
    fields = ('name','description')

    def form_valid(self,form):
        form.instance.creator = self.request.user
        form.instance.save()
        try:
            TeamMember.objects.create(member=self.request.user,team=form.instance)
        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(self.request.user.members.team.name)))
        else:
            messages.success(self.request,"You are now a member of the {} group.".format(self.request.user.members.team.name))

        return super(CreateTeam, self).form_valid(form)



class SingleTeam(generic.DetailView):
    model = Team

#add member
class AddMember(LoginRequiredMixin,generic.edit.FormView):
    template_name = "teams/teamMember_form.html"
    form_class = AddMemberForm

    def form_valid(self,form):
        member = get_object_or_404(User,username=form.cleaned_data["username"])
        team = get_object_or_404(Team,creator=self.request.user)


        try:
            TeamMember.objects.create(member=member,team=team)
        except IntegrityError:
            memberteam = TeamMember.objects.filter(member=member)[0].team
            messages.warning(self.request,("{} is already a member of {}".format(member,memberteam)))
        else:
            messages.success(self.request,"{} is now a member of the {} group.".format(member,team))

        self.success_url = reverse('teams:single',kwargs={'slug':team.slug})
        return super(AddMember, self).form_valid(form)
