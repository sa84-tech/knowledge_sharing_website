from django.shortcuts import get_object_or_404

from mainapp.models import StatusArticle


def post_save(request):
    """фнкция для сохранения статьи в разных статусах"""
    if request.POST.get('under_review'):
        status = get_object_or_404(StatusArticle, name='under_review')
    else:
        status = get_object_or_404(StatusArticle, name='draft')
    return status
