from django.shortcuts import render
from .models import *


def index_page(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, "index.html", context)


def post_page(request, pk):
    context = {
        'post': Post.objects.get(id=pk)
    }
    return render(request, "post.html", context)





