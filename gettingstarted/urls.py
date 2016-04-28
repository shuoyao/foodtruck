from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views


urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^db', hello.views.db, name='db'),
    url(r'^events', hello.views.events, name='events'),
    url(r'^vendors', hello.views.vendors, name='vendors'),
    url(r'^event/(?P<id>[0-9])/$', hello.views.event, name='event'),
    url(r'^vendor/(?P<vid>[0-9])/$', hello.views.v, name='v'),

]
