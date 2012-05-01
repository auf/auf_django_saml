# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django import forms


class RemoteUserForm(forms.Form):
    username = forms.CharField(label=_("Username"), max_length=30)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(RemoteUserForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')

        if username:
            self.user = authenticate(username=username, password=None)
            if self.user is None:
                raise forms.ValidationError("Aucun utilisateur\
                local.")
        return self.cleaned_data

