from django.urls import path
from .views import account

app_name = 'accountapp'

urlpatterns = [
    path('lk/', account, name='account'),
]
