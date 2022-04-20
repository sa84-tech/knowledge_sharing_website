from django.shortcuts import render

from .models import Post, Category, Comment


def index_page(request, category_id=0):

    posts = Post.objects.filter(status__name='published')
    if category_id != 0:
        posts = posts.filter(category=category_id)

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
        'comments': post.comment.all()
    }

    return render(request, "mainapp/post.html", context)
