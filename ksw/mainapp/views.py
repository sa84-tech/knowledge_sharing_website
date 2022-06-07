import json

from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from accountapp.services import check_user
from authapp.models import WriterUserProfile
from .forms import CommentForm, ContentForm
from .models import Post, Comment
from .services.decorators import require_ajax_and_auth
from .services.queries import create_comment, create_post_view, toggle_content_object, get_user_rating, \
    get_user_activity


POSTS_PER_PAGE = 5


def index_page(request, category_id=0, slug=None):
    """Открыть Главную страницу"""
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
    """Открыть страницу статьи"""
    post = get_object_or_404(Post, pk=pk)

    if post.status.name != 'published' and not check_user(request, post.author):
        raise Http404

    author_info = {'rating': get_user_rating(post.author),
                   'activity': get_user_activity(post.author)}
    create_post_view(post, request.user)

    context = {
        'post': post,
        'comments': post.comment.all(),
        'author_info': author_info,
    }

    return render(request, "mainapp/post.html", context)


@require_ajax_and_auth
def add_comment_ajax(request):
    """Создать комментарий"""

    form = CommentForm(json.loads(request.body))
    if form.is_valid():
        form_data = form.cleaned_data
        post = get_object_or_404(Post, pk=form_data['post_id'])
        author_info = get_object_or_404(WriterUserProfile, user=post.author)
        new_comment = create_comment(request.user,
                                     post,
                                     form_data['target_id'],
                                     form_data['target_type'],
                                     form_data['text'])
        if new_comment is not None:
            result = render_to_string(
                'mainapp/includes/inc_comment.html',
                context={'post': post,
                         'comment': new_comment,
                         'author_info': author_info},
                request=request
            )
            return JsonResponse({'result': result, 'total_comments': post.total_comments})


@require_ajax_and_auth
def add_mark_ajax(request):
    """Создать метку (Лайк, Закладка)"""

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


def search(request):

    """Открыть страницу поиска"""
    query = request.GET.get('q')
    sort = request.GET.get('sorting', '-created')
    if sort not in ['created', '-created', 'topic']:
        sort = '-created'

    error_msg = ''

    if not query:
        error_msg = "Пожалуйста, введите ключевое слово"
        return render(request, 'mainapp/search.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(topic__icontains=query) | Q(article__icontains=query)).order_by(sort)

    return render(request, 'mainapp/search.html', {'error_msg': error_msg, 'post_list': post_list, 'query': query})


def help_doc(request):
    """Открыть страницу Помощь"""
    return render(request, "mainapp/help.html")


def archive_filter(request, year, month):
    """Принимает число год и месяц с кнопок блока архива на боковой панели сайта,
    возвращает список всех статей, отсортированных по дате создания, в диапазоне месяца и выбранного года"""

    posts = Post.objects.filter(status__name='published',
                                created__year=year,
                                created__month=month)  # фильтрация по дате и статусу публикации

    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'page_obj': page_obj,
        'title': 'Архив',
    }

    return render(request, "mainapp/index.html", context)
