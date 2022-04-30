from django.shortcuts import get_object_or_404

from authapp.models import WriterUserProfile
from mainapp.models import Post, Like, Comment
from mainapp.services.helpers import get_cti_404


def create_comment(user_id, target_id, target_type, text):
    comment = {
        'object_id': target_id,
        'author_id': user_id,
        'comment': text,
        'content_type_id': get_cti_404(target_type)
    }

    new_comment, is_created = Comment.objects.get_or_create(**comment)
    if is_created:
        new_comment.save()

    return new_comment, is_created


def get_user_rating(user):
    user_profile = get_object_or_404(WriterUserProfile, user=user.pk)
    return user_profile.rating


def toggle_like(user_id, target_id, target_type):

    like = {
        'object_id': target_id,
        'author_id': user_id,
        'content_type_id': get_cti_404(target_type)
    }

    new_like, is_created = Like.objects.get_or_create(**like)

    return new_like.save() if is_created else new_like.delete()


def increase_total_views(post):
    post.total_views += 1
    return post.save()
