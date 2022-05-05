from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from mainapp.models import Post, Comment
from authapp.forms import WriterUserEditForm, WriterUserProfileForm


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


def post_create(request, pk):
    pass


def post_read(request, pk):
    pass


def post_update(request, pk):
    pass


def post_delete(request, pk):
    pass
