from mainapp.models import Like, Comment, Post


def make_user_active(writer_user):
    writer_user.is_active = True
    return writer_user.save()


def get_user_activity(user):

    return 2 * Like.objects.filter(author=user).count() + \
           5 * Comment.objects.filter(author=user).count() + \
           10 * Post.objects.filter(author=user).count()
