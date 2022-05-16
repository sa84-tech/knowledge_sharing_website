from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

from mainapp.models import Post, Comment, StatusArticle
from authapp.forms import WriterUserEditForm, WriterUserProfileForm, PassChangeForm
from authapp.models import WriterUser
from .forms import PostForm
from .models import Bookmark
from .services import post_save


@login_required
def account(request, username):
    user = get_object_or_404(WriterUser, username=username)
    return render(request, "accountapp/account.html", {'target_user': user})


@login_required
def account_posts(request, username, filter_value=None, sort_value=None):
    if request.is_ajax():
        user = get_object_or_404(WriterUser, username=username)
        posts = Post.objects.filter(author=user.pk)

        if user != request.user:
            posts = posts.filter(status__name='published')

        elif filter_value and StatusArticle.objects.filter(name=filter_value).exists():
            posts = posts.filter(status__name=filter_value)

        if sort_value:
            if sort_value in ['created', '-created', 'topic']:
                posts = posts.order_by(sort_value)

        context = {'posts': posts, 'target_user': user}

        result = render_to_string(
            'accountapp/includes/inc_account_posts.html',
            context=context,
            request=request
        )

        return JsonResponse({'result': result})


@login_required
def account_comments(request, username, filter_value=None, sort_value=None):
    if request.is_ajax():
        user = get_object_or_404(WriterUser, username=username)
        comments = Comment.objects.filter(author=user.pk)

        context = {'comments': comments, 'target_user': user}

        result = render_to_string(
            'accountapp/includes/inc_account_comments.html',
            context=context,
            request=request
        )

        return JsonResponse({'result': result})


@login_required
def account_bookmarks(request, username, filter_value=None, sort_value=None):
    if request.is_ajax():
        user = get_object_or_404(WriterUser, username=username)
        bookmarks = Bookmark.objects.filter(author=user.pk)

        if filter_value and filter_value in ['post', 'comment']:
            bookmarks = bookmarks.filter(content_type__model=filter_value)

        if sort_value:
            if sort_value in ['created', '-created', 'topic']:
                bookmarks = bookmarks.order_by(sort_value)

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
