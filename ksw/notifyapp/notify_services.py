from django.forms import model_to_dict
from django.shortcuts import get_list_or_404
from django.urls import reverse
from notifications.models import Notification
from notifications.signals import notify

from authapp.models import WriterUser
from authapp.services.queries import get_moderators
from ksw.settings import MEDIA_URL


def _get_comment_url(comment) -> str:
    """Возвращает url старницы на которой оставлен комментарий comment"""
    post_url = reverse("post_page", kwargs={"pk": comment.post.id})
    return f'{post_url}#comment-{comment.id}'


def _get_post_url(post) -> str:
    """Возвращает url старницы на которой оставлен комментарий comment"""
    post_url = reverse("post_page", kwargs={"pk": post.id})
    return post_url


def comment_signal_handler(sender, instance, created, **kwargs) -> None:
    """Обработчик события сохранения комментария. Создает объект Notification """
    sender = instance.author
    target = instance.content_object
    recipient = instance.content_object.author
    level = 'info'
    verb = 'Комментарий'
    description = ''
    avatar = sender.avatar.url if sender.avatar else f'{MEDIA_URL}seeder/users/no_avatar.jpg'
    target_url = _get_comment_url(instance)

    if instance.body.startswith('@moderator'):
        level = 'danger'
        recipient = get_moderators()
        description = f'Пользователь {instance.author.full_name} сообщил о нарушении.'

    elif type(target).__name__ == 'Comment':
        description = f'Пользователь {instance.author.full_name} ответил на ваш комментарий.'

    elif type(target).__name__ == 'Post':
        description = f'Пользователь {instance.author.full_name} оставил комментарий к вашей статье.'

    notify.send(sender, recipient=recipient, level=level, target=target, verb=verb,
                description=description, sender_avatar=avatar, target_url=target_url)


def post_signal_handler(sender, instance, created, **kwargs):
    if instance.status.name == 'under_review':
        avatar = instance.author.avatar.url if instance.author.avatar else f'{MEDIA_URL}seeder/users/no_avatar.jpg'
        target_url = _get_post_url(instance)
        notify.send(instance.author, recipient=get_moderators(), verb=f'Проверка', target=instance,
                    description=f'Пользователь {instance.author} отправил запрос на публикацию статьи.',
                    sender_avatar=avatar, target_url=target_url, level='danger')


def get_filtered_notifications(user):
    notification = get_list_or_404(
        Notification, recipient=user)
    return notification


def mark_notification_as_read(user: WriterUser, notification_id: int) -> None:
    """Меняет состояние уведомления на Прочитано"""
    notification = Notification.objects.get(recipient=user, id=notification_id)
    if notification:
        notification.mark_as_read()


def get_notification_list(notifications: list[Notification]) -> list[dict]:
    """Возвращает отформатировонный список уведомлений"""

    notification_list = []
    for notification in notifications:
        struct = model_to_dict(notification)
        if notification.actor:
            struct['actor'] = str(notification.actor)
            struct['actor_avatar_src'] = notification.actor.avatar.url \
                if notification.actor.avatar \
                else f'{MEDIA_URL}seeder/users/no_avatar.jpg'
        if notification.target:
            struct['target'] = str(notification.target)
        if notification.action_object:
            struct['action_object'] = str(notification.action_object)
        if notification.data:
            struct['data'] = notification.data

        notification_list.append(struct)

    return notification_list
