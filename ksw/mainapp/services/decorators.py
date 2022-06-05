from functools import wraps
from django.core.exceptions import PermissionDenied


def require_ajax_and_auth(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated:
            return view(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return _wrapped_view
