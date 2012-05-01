
from views import redirect_to_login
from permissions import is_employe
from settings import SAML_REDIRECT_FIELD_NAME

def employe_required(function=None, redirect_field_name=SAML_REDIRECT_FIELD_NAME, login_url=None):
    """
    """
    def _wrapped_view(request, *args, **kwargs):
        if is_employe(request.user):
            return function(request, *args, **kwargs)
        else:
            return redirect_to_login(request, redirect_to=login_url)
    return _wrapped_view
