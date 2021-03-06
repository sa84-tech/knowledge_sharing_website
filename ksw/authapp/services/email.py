from django.core.mail import send_mail, EmailMessage
from django.urls import reverse

from authapp.models import WriterUser
from ksw import settings


def send_verify_mail(user: WriterUser) -> EmailMessage:
    """Отправляет пользователю email с ссылкой активации аккаунта"""
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале ' \
              f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
