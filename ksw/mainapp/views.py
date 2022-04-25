from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from .forms import CommentForm
from mainapp.models import Post, Comment, Category

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index_page(request, category_id=0, slug=None):
    posts = Post.objects.filter(status__name='published')
    if category_id != 0:
        posts = posts.filter(category=category_id)

    paginator = Paginator(posts, 3)  # Show 3 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Главная страница',
        'posts': posts,
        'page_obj': page_obj,
    }

    return render(request, "mainapp/index.html", context)


def post_page(request, pk):

    post = Post.objects.get(id=pk)
    post.total_views += 1
    post.save()

    context = {
        'post': post,
        'comments': post.comment.all()
    }

    return render(request, "mainapp/post.html", context)


@login_required
def add_comment(request, target_type, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():

            comment = {
                'object_id': post.pk,
                'author_id': request.user.pk,
                'comment': form.cleaned_data['comment_text'],
                'content_type_id': get_object_or_404(ContentType, model=target_type).id
            }

            new_comment, is_created = Comment.objects.get_or_create(**comment)
            if is_created:
                new_comment.save()

    return redirect(f'/post/{post.pk}#add_comment')


def add_like(request, pk):
    pass
