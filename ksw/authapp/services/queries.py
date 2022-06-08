from django.shortcuts import get_list_or_404

from authapp.models import WriterUser


def make_user_active(writer_user: WriterUser) -> WriterUser:
    """Задает значение True для свойства is_active у пользователя """
    writer_user.is_active = True
    return writer_user.save()


def get_moderators() -> list[WriterUser]:
    """Возвращает список пользователей с ролью Модератор"""
    return get_list_or_404(WriterUser, is_staff=True)
