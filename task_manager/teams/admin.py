from django.contrib import admin
from . import models
# Register your models here.

class TeamMemberInline(admin.TabularInline):
    model = models.TeamMember

admin.site.register(models.Team)
