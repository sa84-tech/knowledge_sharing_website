from django.urls import path
from .views import login, logout, register, edit, verify
from mainapp.views import index_page


app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('', index_page, name='index_page'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
]
