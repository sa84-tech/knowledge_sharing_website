from django.urls import path
from .views import NotificationsViewList, mark_all_as_read_ajax

app_name = 'notifyapp'

urlpatterns = [
    path('', NotificationsViewList.as_view(), name='notification_page'),
    path('mark-all-as-read', mark_all_as_read_ajax, name='mark_all_as_read'),
]
