from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView

from notifyapp.notify_service import get_filtered_notifications


class NotificationsViewList(ListView):
    """Страница с списком уведомлений пользователя"""
    template_name = 'notifyapp/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return self.request.user.notifications.all().order_by('-timestamp')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationsViewList, self).dispatch(
            request, *args, **kwargs)


@never_cache
def mark_all_as_read_ajax(request):
    if request.user.is_authenticated:
        request.user.notifications.mark_all_as_read()
    return JsonResponse({'success': True})
