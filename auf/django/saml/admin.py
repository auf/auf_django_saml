# -*- coding: utf-8 -*-

from views import redirect_to_login
from django.contrib.admin import site

def saml_login(request, extra_context=None):
    return redirect_to_login(request)


# on recable runtime la fonction qui prend en charge
# le login côté de l'admin pour avoir le même comportement
# que dans le frontend
site.login = saml_login

