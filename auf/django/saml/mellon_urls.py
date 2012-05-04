# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url(r'^sandbox/login$', 'auf.django.saml.views.login_form',
        name='sandbox_login'),
    url(r'^sandbox/logout$', 'auf.django.saml.views.mellon_logout',
        name='sandbox_logout'),
)
