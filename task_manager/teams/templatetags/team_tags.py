from django import template
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from teams.models import TeamMember

register = template.Library()


@register.simple_tag(takes_context=True)
def getteam(context):
    try:
        request = context['request']
        user = User.objects.get(username=request.user.username)
        team = user.userteam
    except ObjectDoesNotExist:
        team = None
    return team
