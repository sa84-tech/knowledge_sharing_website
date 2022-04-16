from django.shortcuts import render
<<<<<<< HEAD
from .models import Post, Category
=======
from .models import *
>>>>>>> d7b24e2af50e6404a84e17d251708ad362d965f7


def index_page(request):

    title = "Главная страница"

    context = {
        'title': title,
        'posts': Post.objects.all(),
        'categories': Category.objects.all()
    }

    return render(request, "mainapp/index.html", context)


def post_page(request, pk):
    context = {
        'post': Post.objects.get(id=pk)
    }
<<<<<<< HEAD
    return render(request, "mainapp/post.html", context)
=======
    return render(request, "post.html", context)





>>>>>>> d7b24e2af50e6404a84e17d251708ad362d965f7
