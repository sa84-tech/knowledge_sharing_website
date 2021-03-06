from functools import wraps
from django.http import JsonResponse


def require_ajax_and_auth(view):
    """Проверяет, что запрос AJAX и пользователь, сделавший запрос, прошел аутентификацию"""

    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if not request.is_ajax():
            return JsonResponse({'status': 'false', 'message': 'Bad request'}, status=400)
        elif not request.user.is_authenticated:
            return JsonResponse({'status': 'false', 'message': 'Unauthorized'}, status=401)
        else:
            return view(request, *args, **kwargs)
    return _wrapped_view
