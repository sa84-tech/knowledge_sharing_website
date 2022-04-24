from django import template

register = template.Library()


@register.simple_tag
def check_like(post, user):
    print('###### post', post)
    if post.is_liked_by(user):
        return 'fa-solid'
    return 'fa-regular'
