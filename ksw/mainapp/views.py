from django.shortcuts import render

from .models import Post, Category, Comment

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index_page(request, category_id=0):

    posts = Post.objects.filter(status__name='published')
    if category_id != 0:
        posts = posts.filter(category=category_id)

    paginator = Paginator(posts, 3)  # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Главная страница',
        'posts': posts,
        'categories': Category.objects.all(),
        'page_obj': page_obj,
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
