from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404


def get_cti(target_type):
    """ Get ContenType id by model name """
    return ContentType.objects.filter(model=target_type).first().id


def get_cti_404(target_type):
    """ Get ContenType id by model name or 404 """
    return get_object_or_404(ContentType, model=target_type).id
