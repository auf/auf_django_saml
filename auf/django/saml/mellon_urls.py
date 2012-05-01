# -*- encoding: utf-8 -*

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    '',
    url(r'^mellon/login$', 'auf.django.saml.views.login_form', ),
    url(r'^mellon/logout$', 'auf.django.saml.views.mellon_logout', ),
)
