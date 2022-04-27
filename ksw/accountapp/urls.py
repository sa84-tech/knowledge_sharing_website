from django.urls import path
from .views import account, product_create, product_read, product_update, product_delete

app_name = 'accountapp'

urlpatterns = [
    path('lk/', account, name='account'),
    path('product_create/', product_create, name='product_create'),
    path('product_read/', product_read, name='product_read'),
    path('product_update/', product_update, name='product_update'),
    path('product_delete/', product_delete, name='product_delete'),
]
