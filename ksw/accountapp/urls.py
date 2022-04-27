from django.urls import path
from .views import account, article_create, article_read, article_update, article_delete

app_name = 'accountapp'

urlpatterns = [
    path('lk/', account, name='account'),
    path('article_create/', article_create, name='article_create'),
    path('article_read/', article_read, name='article_read'),
    path('article_update/', article_update, name='article_update'),
    path('article_delete/', article_delete, name='article_delete'),
]
