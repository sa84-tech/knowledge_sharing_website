from django.shortcuts import render, get_object_or_404

from mainapp.models import Post, Comment


def account(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    return render(request, "accountapp/account.html", {'posts': posts, 'comments': comments})


def post_create(request, pk):
    pass


def post_read(request, pk):
    pass


def post_update(request, pk):
    pass


def post_delete(request, pk):
    pass
