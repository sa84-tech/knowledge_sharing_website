from authapp.models import WriterUser
from mainapp.models import Like, Post, Comment


def get_user_activity(user: WriterUser) -> int:
    """Возвращает значение активности пользователя"""

    return 2 * Like.objects.filter(author=user).count() + \
           5 * Comment.objects.filter(author=user).count() + \
           10 * Post.objects.filter(author=user).count()


def get_user_rating(user: WriterUser) -> int:
    """Возвращает значение рейтинга пользователя"""

    idx = 0
    for post in Post.objects.filter(author=user, status__name='published'):
        idx += post.like.count() + post.comment.count()
    return idx


def get_most_rated() -> list[WriterUser]:
    """Возращает список из четырех самых оактвных пользователей"""

    users = [{'user': user, 'rating': get_user_rating(user)} for user in WriterUser.objects.all()]
    max_rated_users = sorted(users, key=lambda x: x['rating'], reverse=True)[:4]
    return [x['user'] for x in max_rated_users]
