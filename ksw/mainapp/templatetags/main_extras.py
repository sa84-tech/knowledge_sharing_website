from django import template

from ksw.settings import MEDIA_URL

register = template.Library()


@register.simple_tag
def check_like(post, user):
    if post.is_liked_by(user):
        return 'fa-solid'
    return 'fa-regular'


@register.simple_tag
def get_avatar(user):
    return user.avatar.url if user.avatar else f'{MEDIA_URL}seeder/users/no_avatar.jpg'
