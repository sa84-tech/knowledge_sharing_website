from django.urls import path
from .views import NotificationsViewList, mark_all_as_read_ajax, mark_as_read_ajax, get_unread_notification_list

app_name = 'notifyapp'

urlpatterns = [
    path('', NotificationsViewList.as_view(), name='notification_page'),
    path('get-unread-list', get_unread_notification_list, name='get_unread_notification_list'),
    path('mark-all-as-read', mark_all_as_read_ajax, name='mark_all_as_read'),
    path('mark-as-read', mark_as_read_ajax, name='mark_as_read'),
]
