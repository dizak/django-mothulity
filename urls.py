from django.conf.urls import url, include
from . import views


app_name = "mothulity"

urlpatterns = [url(r"^$", views.index, name="index"),
               url(r"^options/$", views.options, name="options"),
               url(r"^submit/$", views.submit, name="submit")]
