
from auf.django.saml import settings

if settings.SAML_AUTH:
    from .admin import AdminTest  # noqa
    from .permissions import PermissionTest  # noqa
    from .template_tags import TemplateTagTest  # noqa
else:
    from .dev import DevTest  # noqa
