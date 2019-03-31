from django.conf.urls import url
from . import views

app_name = "tasks"

urlpatterns = [
    url(r"^$",views.TaskList.as_view(),name="all"),
    url(r"^new/$",views.CreateTask.as_view(),name="create"),
    url(r"^update/(?P<slug>[-\w]+)/$",views.UpdateTask.as_view(),name="update"),
    url(r"^comment/(?P<slug>[-\w]+)/(?P<username>[-\w]+)/$",views.CreateComment.as_view(),name="comment"),
    url(r"^about/(?P<slug>[-\w]+)/$",views.TaskDetail.as_view(),name="single"),
    url(r"^assign/(?P<slug>[-\w]+)/$",views.AssignTask.as_view(),name="assign"),
]
