from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from notifications.models import Notification

from mainapp.services.decorators import require_ajax_and_auth
from notifyapp.notify_services import mark_notification_as_read, get_notification_list


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


@require_ajax_and_auth
def mark_all_as_read_ajax(request):
    request.user.notifications.mark_all_as_read()
    list_html = render_to_string(
        'notifyapp/includes/inc_notification_items.html',
        context={'notifications': request.user.notifications.all()},
        request=request)
    return JsonResponse({'success': True, 'list_html': list_html})


@require_ajax_and_auth
def mark_as_read_ajax(request):
    """Меняет состояние уведомления на Прочитано"""

    notification_id = request.GET.get('id')
    try:
        mark_notification_as_read(request.user, notification_id)
        return JsonResponse({'success': True})
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        return JsonResponse({'status': 'false', 'message': 'Bad request'}, status=400)


@require_ajax_and_auth
def delete_ajax(request):
    """Меняет состояние уведомления на Прочитано"""

    notification_id = request.GET.get('id')
    notification = get_object_or_404(Notification, recipient=request.user, id=notification_id)
    notification.delete()
    return JsonResponse({'success': True})


@require_ajax_and_auth
def get_unread_notification_list(request):
    """Получить список непрочитанных уведомлений пользователя request.user"""

    num_to_fetch = 50
    template = 'mainapp/includes/inc_header_notification_items.html'
    notifications = request.user.notifications.unread()[0:num_to_fetch]

    unread_list_html = render_to_string(
        template,
        context={'notifications': notifications},
        request=request)

    data = {
        'unread_count': request.user.notifications.unread().count(),
        'unread_list_html': unread_list_html,
        'unread_list': get_notification_list(notifications),
    }

    return JsonResponse(data)
