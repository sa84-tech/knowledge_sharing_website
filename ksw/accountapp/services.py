from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404

from authapp.models import WriterUser
from mainapp.models import Post, Comment, StatusArticle
from accountapp.models import Bookmark


def post_save(request) -> StatusArticle:
    """ Возвращает статуса статьи"""

    if request.POST.get('under_review'):
        status = get_object_or_404(StatusArticle, name='under_review')
    else:
        status = get_object_or_404(StatusArticle, name='draft')
    return status


def check_user(request, post_author: WriterUser) -> bool:
    """Возвращает True, если пользователь является автоором статьи или модератором"""

    if request.user == post_author or request.user.is_superuser or request.user.is_staff:
        return True
    return False


def get_sorted_objects(objects: list, sorting_value: str) -> list:
    """Сортирует список объектов по заданному значению"""

    if sorting_value in ['created', '-created', 'topic', 'name', 'body']:
        try:
            return objects.order_by(sorting_value)
        except FieldError:
            print(' *** EXCEPTION sorting_value *** ', sorting_value)
    return objects


def get_filtered_posts(request, user: WriterUser) -> list:
    """Возвращает отсортированный список статей пользователя"""

    posts = Post.objects.filter(author=user.pk).exclude(status__name='deleted')

    filter_value = request.GET.get('filter', None)
    sorting_value = request.GET.get('sorting', '-created')
    if sorting_value == 'name':
        sorting_value = 'topic'

    if user != request.user:
        posts = posts.filter(status__name='published')

    if filter_value and StatusArticle.objects.filter(name=filter_value).exists():
        posts = posts.filter(status__name=filter_value)

    return get_sorted_objects(posts, sorting_value)


def get_filtered_comments(request, user: WriterUser = None) -> list:
    """Возвращает отсортированный список комментариев пользователя"""

    if user is None:
        user = request.user
    comments = Comment.objects.filter(author=user.pk)
    sorting_value = request.GET.get('sorting', '-created')
    if sorting_value == 'name':
        sorting_value = 'body'
    return get_sorted_objects(comments, sorting_value)


def get_filtered_bookmarks(request, user: WriterUser) -> list:
    """Возвращает отсортированный список закладок пользователя"""

    bookmarks = Bookmark.objects.filter(author=user.pk)
    filter_value = request.GET.get('filter', 'post')
    sorting_value = request.GET.get('sorting', '-created')

    if filter_value and filter_value in ['post', 'comment']:
        bookmarks = bookmarks.filter(content_type__model=filter_value)

    return get_sorted_objects(bookmarks, sorting_value)
