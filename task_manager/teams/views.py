from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

from django.urls import reverse
from django.views import generic

from teams.models import Team,TeamMember

# Create your views here.
class CreateTeam(LoginRequiredMixin,PermissionRequiredMixin):
    fields = ('name','description')
    model = Team

class SingleTeam(generic.DetailView):
    model = Team
