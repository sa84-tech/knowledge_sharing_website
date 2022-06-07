# from mainapp.models import Like, Comment, Post
from django.shortcuts import get_list_or_404

from authapp.models import WriterUser


def make_user_active(writer_user):
    """Задать значение True для свойства is_active у WriterUser """
    writer_user.is_active = True
    return writer_user.save()


def get_moderators():
    """Вернуть список пользователей с ролью Модератор"""
    return get_list_or_404(WriterUser, is_staff=True)
