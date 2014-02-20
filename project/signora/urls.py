from django.conf.urls import patterns, url
from signora import views, devices


urlpatterns = patterns('',
                       url(r'^devices/(.*)$', devices.index),)
