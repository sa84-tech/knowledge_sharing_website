def get_user_notifications(request) -> dict:
    """Контекстный процессор. Возвращает словарь со списком непрочитанных уведомлений пользователя"""

    if request.user.is_authenticated:
        return {'notifications': request.user.notifications.unread().order_by('-timestamp')}
    return {'notifications': []}
