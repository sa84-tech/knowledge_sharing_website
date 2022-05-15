from django.urls import path
from .views import account, settings, post_create, post_update, post_delete

app_name = 'accountapp'

urlpatterns = [
    path('lk/', account, name='lk'),
    path('settings/', settings, name='settings'),
    path('post/create/', post_create, name='post_create'),
    path('post/update/<int:pk>/', post_update, name='post_update'),
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),
]
