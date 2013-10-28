# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin

from auf.django.saml.decorators import employe_required, login_required

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^', include('auf.django.saml.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^test_tags/', TemplateView.as_view(template_name="test_tags.html"),
        name='test_tags'),
    url(r'^test_employed_required/',
        employe_required(
            TemplateView.as_view(template_name="test_tags.html")),
        name='test_employe_required'),
    url(r'^test_login_required/',
        login_required(
            TemplateView.as_view(template_name="test_tags.html")),
        name='test_login_required'),
    )
