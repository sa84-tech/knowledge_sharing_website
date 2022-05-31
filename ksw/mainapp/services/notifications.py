from django.shortcuts import get_list_or_404
from notifications.models import Notification
from notifications.signals import notify


def comment_signal_handler(sender, instance, created, **kwargs):
    print('*** INSTANCE NAME:', type(instance).__name__)
    target = instance.content_object
    print('*** TARGET NAME:', type(target).__name__)
    description = ''
    if type(target).__name__ == 'Comment':
        description = 'На ваш комментарий ответили'
    if type(target).__name__ == 'Post':
        description = 'К вашей статье оставили комментарий'
    notify.send(instance.author, recipient=instance.content_object.author,
                target=target, verb='Новый комментарий', description=description)


def post_signal_handler(sender, instance, created, **kwargs):
    notify.send(instance, recipient=instance, verb=f'Статус статьи',
                description=f'Статус статьи {instance.topic} изменился на {instance.status}.')


def get_filtered_notifications(request):
    notification = get_list_or_404(
        Notification, recipient=request.user)
    return notification
