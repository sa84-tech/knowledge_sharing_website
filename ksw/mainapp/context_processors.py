from mainapp.models import Category
from mainapp.services.period_generator import period_generator
from mainapp.services.queries import get_most_rated


def menu(request):
    categories = Category.objects.all()
    return {'categories': categories}


def top4(request):
    top_four = get_most_rated()
    return {'most_rated_users': top_four}


def archive_peroids(request):
    return {'periods': period_generator(request)}
