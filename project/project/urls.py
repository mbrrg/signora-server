from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^signora/', include('signora.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
