from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from .forms import WriterUserLoginForm, WriterUserRegisterForm, WriterUserEditForm, WriterUserProfileForm, \
    EmailChangeForm, PassChangeForm, PassResetForm
from .models import WriterUser
from .services.email import send_verify_mail
from .services.queries import make_user_active


def login(request):
    """Представление. Страница авторизации"""

    title = 'вход'
    login_form = WriterUserLoginForm(data=request.POST or None)

    next_obj = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index_page'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': next_obj,
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    """Представление. Выход из аккаунта"""

    auth.logout(request)
    return HttpResponseRedirect(reverse('index_page'))


def register(request):
    """Представление. Страница регистрации"""

    register_form = WriterUserRegisterForm(data=request.POST or None)

    if request.method == 'POST' and register_form.is_valid():
        user = register_form.save()
        if send_verify_mail(user):
            context = {
                'message_title': 'Активация аккаунта',
                'message_body': f'На адрес {user.email} отправлена ссылка для активации аккаунта.',
                'url_path': 'auth:login',
            }
            return render(request, 'authapp/verification.html', context)

        user.delete()
        register_form.add_error(None, 'Произошла ошибка при попытке отправить ссылку активации. '
                                      'Попробуйте пройти регистрацию позднее.')
    context = {
        'title': 'Регистрация',
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', context)


def edit(request):
    """Представление. Страница настроек пользователя"""

    title = 'профиль'

    if request.method == 'POST':
        edit_form = WriterUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = WriterUserProfileForm(request.POST, instance=request.user.writeruserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = WriterUserEditForm(instance=request.user)
        profile_form = WriterUserProfileForm(instance=request.user.writeruserprofile)
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'accountapp/settings.html', context)


def verify(request, email, activation_key):
    """Представление. Страница с подтверждением регистрации"""

    context = {'title': 'Активация аккаунта'}
    try:
        user = get_object_or_404(WriterUser, email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            make_user_active(user)
            context['message_title'] = 'Регистрация завершена'
            context['message_body'] = f'Пользователь @{user.username} подтвержден.'
            context['url_path'] = 'auth:login'
        else:
            context['message_title'] = 'Ошибка'
            context['message_body'] = f'Активация не пройдена.'
            context['url_path'] = 'auth:register'

        return render(request, 'authapp/verification.html', context)
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('auth:login'))


class PasswordChangeView(PasswordChangeView):
    """Представление. Страница смены пароля"""

    from_class = PassChangeForm
    success_url = reverse_lazy('auth:password_success')


class PassResetView(PasswordResetView):
    """Представление. Страница сброса пароля"""

    form_class = PassResetForm
    template_name = 'authapp/password_reset/password_reset.html'
    subject_template_name = 'authapp/password_reset/password_reset_subject.txt'
    email_template_name = 'authapp/password_reset/password_reset_email.html'
    success_url = reverse_lazy('auth:password_reset_done')


def password_success(request):
    """Представление. Страница с результатом процедуры сброса пароля"""

    return render(request, 'authapp/password_success.html', {})


@login_required
def email_change(request):
    """Представление. Страница для смены Email"""

    if request.method == 'GET':
        form = EmailChangeForm(user=request.user)
    elif request.method == 'POST':
        form = EmailChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('auth:email_success')
    return render(request, 'authapp/update_email.html', {'form': form})


def email_success(request):
    """Представление. Страница с результатами процедуры сброса Email"""

    return render(request, 'authapp/email_success.html', {})
