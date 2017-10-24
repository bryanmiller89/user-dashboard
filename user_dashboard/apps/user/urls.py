from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'user/(?P<user_id>.*)$', views.show),
    url(r'message/(?P<receiver_id>.*)$', views.message),
    url(r'comment/(?P<message_id>.*)/(?P<receiver_id>.*)$', views.comment),
]
