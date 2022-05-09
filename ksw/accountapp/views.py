from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from mainapp.models import Post, Comment
from authapp.forms import WriterUserEditForm, WriterUserProfileForm, PassChangeForm


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


def post_create(request, pk):
    pass


def post_read(request, pk):
    pass


def post_update(request, pk):
    pass


def post_delete(request, pk):
    pass
