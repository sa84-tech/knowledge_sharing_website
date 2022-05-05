from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from mainapp.models import Post, Comment
from authapp.forms import WriterUserEditForm, WriterUserProfileForm

from .forms import PostForm


@login_required
def account(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, "accountapp/account.html", {'posts': posts, 'comments': comments})


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
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'accountapp/settings.html', context)

    # return render(request, "accountapp/settings.html", {'posts': posts, 'comments': comments})


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index_page')
    else:
        form = PostForm()

    context = {
        'form': form,
        'post_list': Post.objects.filter(author=request.user)
    }
    return render(request, 'accountapp/post_create.html', context)


def post_read(request, pk):
    pass


def post_update(request, pk):
    edit_post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        edit_form = PostForm(request.POST, request.FILES, instance=edit_post)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('account:post_create')
    else:
        edit_form = PostForm(instance=edit_post)
    context = {'update_form': edit_form}
    return render(request, 'accountapp/post_update.html', context)


def post_delete(request, pk):
    pass
