from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify

from teams.models import Team
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=255,unique=True)
    description = models.TextField(blank=True,default='')

    STATUS_CHOICES = (
        ("PLANNED", "Planned"),
        ("INPROGRESS", "Inprogress"),
        ("DONE", "Done"),
    )
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default="PLANNED")

    slug = models.SlugField(allow_unicode=True,unique=True)
    creator = models.ForeignKey(User,related_name="tasks",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    assignees = models.ManyToManyField(User,through="TaskAssignees")

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("tasks:single",kwargs={'slug':self.slug})

    class Meta:
        ordering = ["-created_at"]


class TaskAssignees(models.Model):
    task = models.ForeignKey(Task,related_name="assigned",on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name="user_task",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("task","user")

class TaskTeam(models.Model):
    task = models.ForeignKey(Task,related_name="tasks",on_delete=models.CASCADE)
    team = models.ForeignKey(Team,related_name="team",on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name

    class Meta:
        unique_together = ("team","task")

class Comment(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User,related_name="user_comments",on_delete=models.CASCADE)
    task = models.ForeignKey(Task,related_name="task_comments",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("tasks:single",kwargs={'slug':task.slug})

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("message","user")
