from django.conf.urls import url, include
from . import views


app_name = "mothulity"

urlpatterns = [url(r"^$", views.index, name="index"),
               url(r"^submit/(?P<job>.+)$", views.submit, name="submit"),
               url(r"^status/(?P<job>.+)$", views.status, name="status"),
               url(r"^wiki/(?P<title>.+)$", views.wiki, name="wiki")]
