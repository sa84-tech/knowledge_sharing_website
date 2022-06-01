from django.shortcuts import get_list_or_404
from notifications.models import Notification
from notifications.signals import notify


def comment_signal_handler(sender, instance, created, **kwargs):
    sender = instance.author
    target = instance.content_object
    level = 'info'
    description = ''
    recipient = instance.content_object.author
    if type(target).__name__ == 'Comment':
        if target.body.startswith('@moderator'):
            description = f'{target.body}'
            level = 'danger'
            recipient = type(target.author).objects.filter(is_staff=True)
            print('@@@ recipient:', recipient)
            print('@@@ description:', description)
        else:
            description = f'Пользователь {instance.author.full_name} ответил на ваш комментарий'

    elif type(target).__name__ == 'Post':
        description = f'Пользователь {instance.author.full_name} оставил комментарий к вашей статье.'

    notify.send(sender, recipient=recipient, level=level,
                target=target, verb='Комментарий', description=description)


def post_signal_handler(sender, instance, created, **kwargs):
    notify.send(instance, recipient=instance, verb=f'Статус статьи',
                description=f'Статус статьи {instance.topic} изменился на {instance.status}.')


def get_filtered_notifications(user):
    notification = get_list_or_404(
        Notification, recipient=user)
    return notification
