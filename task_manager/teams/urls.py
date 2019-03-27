from django.conf.urls import url
from . import views

app_name = "teams"

urlpatterns = [
    url(r'^about/(?P<slug>[-\w]+)/$',views.SingleTeam.as_view(),name='single'),
    url(r'^new/$',views.CreateTeam.as_view(),name='create'),
    url(r'^add/$',views.AddMember.as_view(),name='add_member'),
]
