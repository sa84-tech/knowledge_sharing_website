from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from authapp.models import WriterUser
from mainapp.models import Post, Like, Comment, View
from accountapp.models import Bookmark


def create_comment(user: WriterUser, post: Post, target_id: int, target_type: str, comment_body: str) -> Comment:
    """ Создает новый комментарий """
    comment = {
        'post': post,
        'object_id': target_id,
        'author': user,
        'body': comment_body,
        'content_type_id': get_object_or_404(ContentType, model=target_type).id
    }

    new_comment = Comment(**comment)
    new_comment.save()

    return new_comment


def toggle_content_object(user: WriterUser, target_type: str, target_id: str, model_name: str) -> int:
    """Создает новый объект (тип Like/Bookmark) для статьи или комментария,
       если объект уже существует, удаляет его.
    """
    models = {'like': Like, 'bookmark': Bookmark}

    target_ct = get_object_or_404(ContentType, model=target_type)
    target_obj = get_object_or_404(target_ct.model_class(), pk=target_id)
    new_obj, is_created = models[model_name].objects.get_or_create(object_id=target_obj.pk,
                                                                   author=user,
                                                                   content_type=target_ct)
    if is_created:
        new_obj.save()
    else:
        new_obj.delete()
    return target_obj.total_bookmarks if model_name == 'bookmark' else target_obj.total_likes


def create_post_view(post: Post, user) -> None:
    """ Создает объект просмотра """

    if user.is_authenticated:
        view_dict = {
            'object_id': post.pk,
            'author_id': user.id,
            'content_type': get_object_or_404(ContentType, model='post')
        }

        new_view, is_created = View.objects.get_or_create(**view_dict)

        if is_created:
            new_view.save()
