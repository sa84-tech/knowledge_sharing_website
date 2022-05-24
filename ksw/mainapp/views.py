import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from authapp.models import WriterUserProfile
from .forms import CommentForm, ContentForm
from .models import Post
from .services.queries import get_user_rating, create_comment, create_post_view, toggle_content_object

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
    create_post_view(post, request.user)

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


def content_btn_handler(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            form = ContentForm(json.loads(request.body))

            if form.is_valid():
                form_data = form.cleaned_data
                post = get_object_or_404(Post, pk=form_data['post_id'])
                counter_value = toggle_content_object(request.user, form_data['target_type'],
                                                      form_data['target_id'], form_data['btn_type'])
                if counter_value is not None:
                    user_rating = get_user_rating(post.author)
                    return JsonResponse({'counter_value': counter_value,
                                         'user_rating': user_rating})
        else:
            return JsonResponse({'status': 'false', 'message': 'Unauthorized'}, status=401)

    return JsonResponse({'status': 'false', 'message': 'Bad request'}, status=400)



def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "Пожалуйста, введите ключевое слово"
        return render(request, 'mainapp/search.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(topic__icontains=q) | Q(article__icontains=q))
    return render(request, 'mainapp/search.html', {'error_msg': error_msg, 'post_list': post_list})
