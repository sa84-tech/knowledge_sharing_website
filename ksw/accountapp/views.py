from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from .forms import PostForm
from .services import post_save, get_filtered_posts, get_filtered_comments, get_filtered_bookmarks, check_user
from gradeapp.grade_services import get_user_rating, get_user_activity
from mainapp.services.decorators import require_ajax_and_auth
from authapp.forms import WriterUserEditForm, WriterUserProfileForm, PasswordChangeForm, EmailChangeForm
from authapp.models import WriterUser
from authapp.forms import PassChangeForm
from mainapp.models import Post, StatusArticle


@login_required
def account(request, username: str) -> HttpResponse:
    """Представление. Возвращает страницу Личного кабинета"""

    user = get_object_or_404(WriterUser, username=username)
    user_info = {'rating': get_user_rating(user),
                 'activity': get_user_activity(user)}
    return render(request, "accountapp/account.html", {'target_user': user, 'user_info': user_info})


@require_ajax_and_auth
def account_posts(request, username: str) -> JsonResponse:
    """Представление AJAX. Возвращает Html-разметку со списком статей пользователя"""

    user = get_object_or_404(WriterUser, username=username)
    posts = get_filtered_posts(request, user)

    context = {'posts': posts, 'target_user': user}

    result = render_to_string(
        'accountapp/includes/inc_account_posts.html',
        context=context,
        request=request
    )

    return JsonResponse({'result': result})


@require_ajax_and_auth
def account_comments(request, username: str) -> JsonResponse:
    """Представление AJAX. Возвращает Html-разметку со списком комментариев пользователя"""

    user = get_object_or_404(WriterUser, username=username)
    comments = get_filtered_comments(request, user)
    context = {'comments': comments, 'target_user': user}

    result = render_to_string(
        'accountapp/includes/inc_account_comments.html',
        context=context,
        request=request
    )

    return JsonResponse({'result': result})


@require_ajax_and_auth
def account_bookmarks(request, username: str) -> JsonResponse:
    """Представление AJAX. Возвращает Html-разметку со списком закладок пользователя"""

    user = get_object_or_404(WriterUser, username=username)
    bookmarks = get_filtered_bookmarks(request, user)

    context = {'bookmarks': bookmarks, 'target_user': user}

    result = render_to_string(
        'accountapp/includes/inc_account_bookmarks.html',
        context=context,
        request=request
    )

    return JsonResponse({'result': result})


class SettingsView(LoginRequiredMixin, TemplateView):
    """Представление. Страница настроек пользователя"""

    template_name = 'accountapp/settings.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(edit_form=WriterUserEditForm(instance=request.user),
                                        profile_form=WriterUserProfileForm(instance=request.user.writeruserprofile),
                                        password_form=PassChangeForm(request.user),
                                        email_form=EmailChangeForm(user=request.user), **kwargs)
        return self.render_to_response(context)


class UserProfileView(LoginRequiredMixin, FormView):
    """Представление. Обрабатывает POST-запрос для страницы редактирования профиля пользователя"""

    form_class = WriterUserEditForm
    template_name = 'accountapp/settings.html'
    success_url = reverse_lazy('account:settings', args=('profile-success',))

    def post(self, request, *args, **kwargs):
        edit_form = WriterUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = WriterUserProfileForm(request.POST, instance=request.user.writeruserprofile)
        password_form = PassChangeForm(request.user)
        email_form = EmailChangeForm(user=request.user)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            profile_form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            context = self.get_context_data(**kwargs, edit_form=edit_form, profile_form=profile_form,
                                            password_form=password_form, email_form=email_form, page='profile')
            return self.render_to_response(context)


class PassChangeView(LoginRequiredMixin, PasswordChangeView):
    """Представление. Обрабатывает POST-запрос для страницы изменения пароля пользователя"""

    form_class = PasswordChangeForm
    template_name = 'accountapp/settings.html'
    success_url = reverse_lazy('account:settings', args=('password-success',))

    def post(self, request, *args, **kwargs):
        edit_form = WriterUserEditForm(instance=request.user)
        profile_form = WriterUserProfileForm(instance=request.user.writeruserprofile)
        password_form = PassChangeForm(request.user, request.POST)
        email_form = EmailChangeForm(user=request.user)
        if password_form.is_valid():
            password_form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            context = self.get_context_data(**kwargs, edit_form=edit_form, profile_form=profile_form,
                                            password_form=password_form, email_form=email_form, page='password')
            return self.render_to_response(context)


class EmailChangeView(LoginRequiredMixin, FormView):
    """Представление. Обрабатывает POST-запрос для страницы изменения эл. почты пользователя"""

    form_class = EmailChangeForm
    template_name = 'accountapp/settings.html'
    success_url = reverse_lazy('account:settings', args=('email-success',))

    def post(self, request, *args, **kwargs):
        edit_form = WriterUserEditForm(instance=request.user)
        profile_form = WriterUserProfileForm(instance=request.user.writeruserprofile)
        password_form = PassChangeForm(request.user)
        email_form = EmailChangeForm(user=request.user, data=request.POST)
        if email_form.is_valid():
            email_form.save()
            return HttpResponseRedirect(self.success_url)
        else:
            context = {'edit_form': edit_form,
                       'profile_form': profile_form,
                       'password_form': password_form,
                       'email_form': email_form,
                       'page': 'email'}
            return self.render_to_response(context)


@login_required
def post_create(request) -> HttpResponse:
    """Представление. Страница для создания статьи"""

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.status = post_save(request)
            new_post.save()
            return redirect('account:lk', request.user)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'accountapp/post_edit.html', context)


@login_required
def post_update(request, pk: int) -> [HttpResponse, HttpResponseRedirect]:
    """Представление. Страница для редактирования статьи"""

    edit_post = get_object_or_404(Post, pk=pk)
    if check_user(request, edit_post.author):
        if request.method == 'POST':
            edit_form = PostForm(request.POST, request.FILES, instance=edit_post)
            if edit_form.is_valid():
                edit_post.status = post_save(request)
                edit_form.save()
                return redirect('account:lk', request.user)
        else:
            edit_form = PostForm(instance=edit_post)
        context = {'form': edit_form, 'post': edit_post}
        return render(request, 'accountapp/post_edit.html', context)
    else:
        return redirect('account:lk', request.user)


@login_required
def post_delete(request, pk: int) -> [HttpResponse, HttpResponseRedirect]:
    """Представление. Страница для удаления статьи"""

    delete_post = get_object_or_404(Post, pk=pk)
    if check_user(request, delete_post.author):
        if request.method == 'POST':
            delete_post.status = get_object_or_404(StatusArticle, name='deleted')
            delete_post.save()
            return redirect('account:lk', request.user)
        context = {'form': delete_post, 'target_user': request.user}
        return render(request, 'accountapp/post_delete.html', context)
    else:
        return redirect('account:lk', request.user)
