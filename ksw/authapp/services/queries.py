def make_user_active(writer_user):
    writer_user.is_active = True
    return writer_user.save()
