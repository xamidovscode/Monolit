from . import views
from django.urls import re_path


urlpatterns = [
    re_path('^$', views.index),
    re_path('^register$', views.register),
    re_path('^success$', views.success),
    re_path('^reset$', views.reset),
    re_path('^wall$', views.wall),
]