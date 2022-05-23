from django import template

from ksw.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def check_like(post, user):
    if post.has_relation_with(user, 'like'):
        return 'fa-solid shadow'
    return 'fa-regular'


@register.simple_tag
def check_bookmark(post, user):
    if post.has_relation_with(user, 'bookmark'):
        return 'fa-solid shadow'
    return 'fa-regular'


@register.simple_tag
def check_comment(post, user):
    if post.has_relation_with(user, 'comment'):
        return 'fa-solid shadow'
    return 'fa-regular'


@register.simple_tag
def check_view(post, user):
    if post.has_relation_with(user, 'view'):
        return 'fa-solid shadow'
    return 'fa-regular'


@register.simple_tag
def get_avatar(user):
    return user.avatar.url if user.avatar else f'{MEDIA_URL}seeder/users/no_avatar.jpg'
