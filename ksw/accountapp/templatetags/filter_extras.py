from django import template
from django.template.defaultfilters import stringfilter

from ..constant import status_post_const

register = template.Library()


@register.filter
@stringfilter
def filter_post_status(key):
    return status_post_const[key]


register.filter('filter_post_status', filter_post_status)
