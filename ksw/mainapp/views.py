import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from authapp.models import WriterUserProfile
from .forms import CommentForm, ContentForm
from .models import Post, StatusArticle
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
    # sort = request.GET.get('order_by', '-created')
    # if sort not in ['created', '-created', 'view', 'like']:
    #     sort = '-created'
    error_msg = ''

    if not q:
        error_msg = "Пожалуйста, введите ключевое слово"
        return render(request, 'mainapp/search.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(topic__icontains=q) | Q(article__icontains=q)).order_by('-created')
    # post_list = Post.objects.filter(Q(topic__icontains=q) | Q(article__icontains=q))
    print(post_list)
    return render(request, 'mainapp/search.html', {'error_msg': error_msg, 'post_list': post_list})


# def search_ajax(request):
#     if request.is_ajax():
#         q = request.GET.get('q')
#         sort = request.GET.get('order_by', '-created')
#         if sort not in ['created', '-created', 'view', 'like']:
#             sort = '-created'
#
#         post_list = Post.objects.filter(Q(topic__icontains=q) | Q(article__icontains=q)).order_by(sort)
#
#         context = {'post_list': post_list}
#
#         result = render_to_string(
#             'mainapp/search.html',
#             context=context,
#             request=request
#         )
#
#         return JsonResponse({'result': result})


def get_sorted_objects(objects, sorting_value):
    if sorting_value in ['created', '-created', 'topic', 'name']:
        try:
            return objects.order_by(sorting_value)
        except FieldError:
            print(' *** EXCEPTION sorting_value *** ', sorting_value)
    return objects


def get_filtered_posts(request):
    posts = Post.objects.filter(status__name='published')

    filter_value = request.GET.get('filter', None)
    sorting_value = request.GET.get('sorting', '-created')
    if sorting_value == 'rating':
        sorting_value = 'like'

    if filter_value and StatusArticle.objects.filter(name=filter_value).exists():
        posts = posts.filter(status__name=filter_value)

    return get_sorted_objects(posts, sorting_value)


def search_ajax(request):
    if request.is_ajax():

        posts = get_filtered_posts(request)

        # Это только для проверкы работы фронтенда, нужно удалить!
        posts = Post.objects.all()
        context = {'post_list': posts}

        result = render_to_string(
            'mainapp/includes/inc_search_items.html',
            context=context,
            request=request
        )

        return JsonResponse({'result': result})


def help_doc(request):
    return render(request, "mainapp/help.html")
