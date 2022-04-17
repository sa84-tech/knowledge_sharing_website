from django.shortcuts import render

from .models import Post, Category


def index_page(request, category_id=0):

    if category_id:
        posts = Post.objects.filter(status__name='published', category=category_id).order_by('-created')
    else:
        posts = Post.objects.filter(status__name='published').order_by('-created')

    context = {
        'title': 'Главная страница',
        'posts': posts,
        'categories': Category.objects.all(),
    }

    return render(request, "mainapp/index.html", context)


def post_page(request, pk):

    post = Post.objects.get(id=pk)
    post.total_views += 1
    post.save()

    context = {
        'post': post,
        'categories': Category.objects.all(),
    }

    return render(request, "mainapp/post.html", context)
