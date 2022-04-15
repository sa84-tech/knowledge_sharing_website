from django.shortcuts import render
from .models import Post, Category


def index_page(request):

    title = "Главная страница"

    context = {
        'title': title,
        'posts': Post.objects.all(),
        'categories': Category.objects.all()
    }

    return render(request, "mainapp/index.html", context)


def post_page(request, post_id):
    context = {
        'post': Post.objects.get(id=post_id)
    }
    return render(request, "mainapp/post.html", context)
