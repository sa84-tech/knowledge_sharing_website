from mainapp.models import Category
from authapp.models import WriterUserProfile
from mainapp.services.period_generator import period_generator


def menu(request):
    categories = Category.objects.all()
    return {'categories': categories}


def top4(request):
    top_four = WriterUserProfile.get_most_rated(4)
    return {'most_rated_users': top_four}


def archive_peroids(request):
    return {'periods': period_generator(request)}
