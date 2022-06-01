def get_user_notifications(request):
    if request.user.is_authenticated:
        return {'notifications': request.user.notifications.all().order_by('-timestamp')}
    return {'notifications': []}
