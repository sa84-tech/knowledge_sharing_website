from django.urls import path
from .views import account, settings, post_create, post_update, post_delete, account_posts, account_comments, \
    account_bookmarks

app_name = 'accountapp'

urlpatterns = [
    path('lk/', account, name='lk'),
    path('users/<str:username>/', account, name='lk'),
    path('api/users/<str:username>/posts/', account_posts, name='lk_posts'),
    path('api/users/<str:username>/comments/', account_comments, name='lk_comments'),
    path('api/users/<str:username>/bookmarks/', account_bookmarks, name='lk_bookmarks'),
    path('settings/', settings, name='settings'),
    path('post/create/', post_create, name='post_create'),
    path('post/update/<int:pk>/', post_update, name='post_update'),
    path('post/delete/<int:pk>/', post_delete, name='post_delete'),
]
