from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from mainapp.models import Post, Comment, StatusArticle
from authapp.forms import WriterUserEditForm, WriterUserProfileForm, PassChangeForm

from .forms import PostForm
from .services import post_save


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
    password_form = PassChangeForm(request.user)
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'accountapp/settings.html', context)

    # return render(request, "accountapp/settings.html", {'posts': posts, 'comments': comments})


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
            return redirect('account:lk')
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
            return redirect('account:lk')
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
            return HttpResponseRedirect(reverse('account:lk'))
        context = {'form': delete_post}
        return render(request, 'accountapp/post_delete.html', context)
    else:
        return redirect('account:lk')