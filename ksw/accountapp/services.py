from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404

from mainapp.models import Post, Comment, StatusArticle
from accountapp.models import Bookmark


def post_save(request):
    """ функция для сохранения статьи в разных статусах """
    if request.POST.get('under_review'):
        status = get_object_or_404(StatusArticle, name='under_review')
    else:
        status = get_object_or_404(StatusArticle, name='draft')
    return status


def get_sorted_objects(objects, request):
    sorting_value = request.GET.get('sorting', '-created')
    if sorting_value and sorting_value in ['created', '-created', 'topic', 'name']:
        try:
            return objects.order_by(sorting_value)
        except FieldError:
            return objects.order_by('topic')  # временное решение
    return objects


def get_filtered_posts(request, user):
    posts = Post.objects.filter(author=user.pk).exclude(status__name='deleted')

    filter_value = request.GET.get('filter', None)

    if user != request.user:
        posts = posts.filter(status__name='published')

    if filter_value and StatusArticle.objects.filter(name=filter_value).exists():
        posts = posts.filter(status__name=filter_value)

    return get_sorted_objects(posts, request)


def get_filtered_comments(request, user):
    comments = Comment.objects.filter(author=user.pk)
    return get_sorted_objects(comments, request)


def get_filtered_bookmarks(request, user):
    bookmarks = Bookmark.objects.filter(author=user.pk)
    filter_value = request.GET.get('filter', None)

    if filter_value and filter_value in ['post', 'comment']:
        bookmarks = bookmarks.filter(content_type__model=filter_value)

    return get_sorted_objects(bookmarks, request)
