from django.conf.urls import url
from . import views

app_name = "tasks"

urlpatterns = [
    url(r"^$",views.TaskList.as_view(),name="all"),
    url(r"^new/$",views.CreateTask.as_view(),name="create"),
    url(r"^about/(?P<slug>[-\w]+)/$",views.TaskDetail.as_view(),name="single"),
    url(r"^assign/$",views.AssignTask.as_view(),name="assign"),
]
