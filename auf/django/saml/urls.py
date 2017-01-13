# -*- encoding: utf-8 -*

from django.conf.urls import patterns, url

import monkey


urlpatterns = patterns(
    '',
    url(r'^logout/$', 'auf.django.saml.views.local_logout',
        name='local_logout'),
    url(r'^admin/password_change/$', 'auf.django.saml.views.password_change',
        name='password_change'),
)
