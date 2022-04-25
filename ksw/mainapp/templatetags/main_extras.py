from django import template

register = template.Library()


@register.simple_tag
def check_like(post, user):
    if post.is_liked_by(user):
        return 'fa-solid'
    return 'fa-regular'


@register.simple_tag
def get_avatar(user):
    return user.avatar if user.avatar else '/media/seeder/users/no_avatar.jpg'
