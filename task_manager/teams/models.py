from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register = template.Library()
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    creator = models.OneToOneField(User,related_name="userteam",on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('teams:single',kwargs={'slug':self.slug})

class TeamMember(models.Model):
    team = models.ForeignKey(Team,related_name="memberships",on_delete=models.CASCADE)
    member = models.OneToOneField(User,related_name="members",on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name

    class Meta:
        unique_together = ("team","member")
