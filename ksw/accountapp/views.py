from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from mainapp.models import Post, Comment, StatusArticle
from authapp.forms import WriterUserEditForm, WriterUserProfileForm, PassChangeForm
from authapp.models import WriterUser
from .forms import PostForm
from .services import post_save, get_filtered_posts, get_filtered_comments, get_filtered_bookmarks


@login_required
def account(request, username):
    user = get_object_or_404(WriterUser, username=username)
    return render(request, "accountapp/account.html", {'target_user': user})


@login_required
def account_posts(request, username):
    if request.is_ajax():
        user = get_object_or_404(WriterUser, username=username)
        posts = get_filtered_posts(request, user)

        context = {'posts': posts, 'target_user': user}

        result = render_to_string(
            'accountapp/includes/inc_account_posts.html',
            context=context,
            request=request
        )

        return JsonResponse({'result': result})


@login_required
def account_comments(request, username):
    if request.is_ajax():
        user = get_object_or_404(WriterUser, username=username)
        comments = get_filtered_comments(request, user)

        context = {'comments': comments, 'target_user': user}

        result = render_to_string(
            'accountapp/includes/inc_account_comments.html',
            context=context,
            request=request
        )

        return JsonResponse({'result': result})


@login_required
def account_bookmarks(request, username):
    if request.is_ajax():
        user = get_object_or_404(WriterUser, username=username)
        bookmarks = get_filtered_bookmarks(request, user)

        context = {'bookmarks': bookmarks, 'target_user': user}

        result = render_to_string(
            'accountapp/includes/inc_account_bookmarks.html',
            context=context,
            request=request
        )

        return JsonResponse({'result': result})


@login_required
def settings(request):

    title = 'профиль'

    if request.method == 'POST':
        edit_form = WriterUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = WriterUserProfileForm(request.POST, instance=request.user.writeruserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('account:settings'))
    else:
        edit_form = WriterUserEditForm(instance=request.user)
        profile_form = WriterUserProfileForm(instance=request.user.writeruserprofile)
    password_form = PassChangeForm(request.user)
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'accountapp/settings.html', context)


class PassChangeView(PasswordChangeView):
    from_class = PassChangeForm
    success_url = reverse_lazy('auth:password_success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(user=self.request.user)
        return kwargs

    def form_valid(self, form):
        return JsonResponse({'foo': 'bar'})


@login_required
def post_create(request):
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
def post_update(request, pk):
    edit_post = get_object_or_404(Post, pk=pk)
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


@login_required
def post_delete(request, pk):
    delete_post = get_object_or_404(Post, pk=pk)
    if request.user == delete_post.author or request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            delete_post.status = get_object_or_404(StatusArticle, name='deleted')
            delete_post.save()
            return HttpResponseRedirect(reverse('account:lk', request.user))
        context = {'form': delete_post}
        return render(request, 'accountapp/post_delete.html', context)
    else:
        return redirect('account:lk', request.user)
