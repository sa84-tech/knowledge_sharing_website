import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from authapp.models import WriterUserProfile
from .forms import CommentForm, LikeForm
from .models import Post
from .services.queries import toggle_like, get_user_rating, create_comment, increase_total_views, toggle_bookmark

POSTS_PER_PAGE = 5


def index_page(request, category_id=0, slug=None):
    posts = Post.objects.filter(status__name='published')
    if slug:
        posts = posts.filter(category__slug=slug)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Главная страница',
        'posts': posts,
        'page_obj': page_obj,
    }

    return render(request, "mainapp/index.html", context)


def post_page(request, pk):

    post = get_object_or_404(Post, pk=pk)
    author_info = get_object_or_404(WriterUserProfile, user=post.author)
    increase_total_views(post)

    context = {
        'post': post,
        'comments': post.comment.all(),
        'author_info': author_info,
    }

    return render(request, "mainapp/post.html", context)


@login_required
def add_comment(request, target_type, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['comment_text']
            create_comment(request.user.pk, post.pk, target_type, comment_text)

    return redirect(f'/post/{post.pk}#add_comment')


def add_like(request):

    if request.user.is_authenticated:
        form = LikeForm(json.loads(request.body))

        if form.is_valid():
            form_data = form.cleaned_data
            post = get_object_or_404(Post, pk=form_data['target_id'])
            toggle_like(request.user.pk, post.pk, form_data['target_type'])

            return JsonResponse({'total_likes': post.total_likes, 'user_rating': get_user_rating(post.author)})

    return JsonResponse({'status': 'false', 'message': 'Bad request'}, status=400)


def add_bookmark(request):

    if request.user.is_authenticated:
        form = LikeForm(json.loads(request.body))

        if form.is_valid():
            form_data = form.cleaned_data
            post = get_object_or_404(Post, pk=form_data['target_id'])
            toggle_bookmark(request.user.pk, post.pk, form_data['target_type'])

            return JsonResponse({'total_bookmarks': post.total_bookmarks, 'user_rating': get_user_rating(post.author)})

    return JsonResponse({'status': 'false', 'message': 'Bad request'}, status=400)
