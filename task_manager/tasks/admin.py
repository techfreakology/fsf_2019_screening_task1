from django.contrib import admin

from . import models

# Register your models here.
class TaskAssigneesInline(admin.TabularInline):
    model = models.TaskAssignees

class TaskTeamInline(admin.TabularInline):
    model = models.TaskTeam

admin.site.register(models.Task)
