from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import login, logout, register, edit, verify, PasswordChangeView, password_success, \
    email_change, email_success, PassResetView
from mainapp.views import index_page

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    path('', index_page, name='index_page'),
    path('verify/<str:email>/<str:activation_key>/', verify, name='verify'),
    path('password/', PasswordChangeView.as_view(template_name='authapp/change_password.html'), name='change_password'),
    path('password-success/', password_success, name='password_success'),
    path('password-reset/', PassResetView.as_view(), name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='authapp/password_reset/password_reset_mail_sent.html'
         ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='authapp/password_reset/password_reset_confirmation.html',
             success_url=reverse_lazy('auth:password_reset_complete')
         ), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='authapp/password_reset/password_reset_completed.html'
         ), name='password_reset_complete'),
    path('update-email/', email_change, name='update_email'),
    path('email-success/', email_success, name='email_success'),
]
