from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import WriterUserLoginForm, WriterUserRegisterForm, WriterUserEditForm, WriterUserProfileForm


def login(request):
    title = 'вход'
    login_form = WriterUserLoginForm(data=request.POST or None)

    next_obj = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
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
    auth.logout(request)
    return HttpResponseRedirect(reverse('index_page'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = WriterUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = WriterUserRegisterForm()
    context = {
        'title': title,
        'register_form': register_form}
    return render(request, 'authapp/register.html', context)


def edit(request):
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
    return render(request, 'authapp/edit.html', context)
