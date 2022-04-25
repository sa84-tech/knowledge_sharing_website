import json

from django.contrib.auth.decorators import login_required
from django.http import  JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .forms import CommentForm, LikeForm
from .models import Post, Comment, Like
from .services.helpers import get_cti_404
from authapp.models import WriterUser, WriterUserProfile


POSTS_PER_PAGE = 5


def index_page(request, category_id=0):

    posts = Post.objects.filter(status__name='published')
    if category_id != 0:
        posts = posts.filter(category=category_id)

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Главная страница',
        'posts': posts,
        'page_obj': page_obj,
        'most_rated_users': WriterUserProfile.get_most_rated(4)
    }

    return render(request, "mainapp/index.html", context)


def post_page(request, pk):

    post = Post.objects.get(id=pk)
    post.total_views += 1
    post.save()

    activity = WriterUserProfile.objects.filter(user=post.author)

    context = {
        'post': post,
        'comments': post.comment.all(),
        'activity': activity,
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
                'content_type_id': get_cti_404(target_type)
            }

            new_comment, is_created = Comment.objects.get_or_create(**comment)
            if is_created:
                new_comment.save()

    return redirect(f'/post/{post.pk}#add_comment')


def add_like(request):

    if request.user.is_authenticated:

        form = LikeForm(json.loads(request.body))

        if form.is_valid():
            cd = form.cleaned_data
            post = get_object_or_404(Post, pk=cd['target_pk'])

            like = {
                'object_id': post.pk,
                'author_id': request.user.pk,
                'content_type_id': get_cti_404(cd['target_type'])
            }

            new_like, is_created = Like.objects.get_or_create(**like)
            new_like.save() if is_created else new_like.delete()

            return JsonResponse({'total_likes': post.total_likes})

    return JsonResponse({'status': 'false', 'message': 'Bad request'}, status=400)
