from django.urls import path
from .views import account, settings, post_create, post_read, post_update, post_delete

app_name = 'accountapp'

urlpatterns = [
    path('lk/', account, name='lk'),
    path('settings/', settings, name='settings'),
    path('post_create/', post_create, name='post_create'),
    path('post_read/', post_read, name='post_read'),
    path('<int:pk>/post_update/', post_update, name='post_update'),
    path('post_delete/', post_delete, name='post_delete'),
]
