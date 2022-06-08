from gradeapp.grade_services import get_most_rated
from mainapp.models import Category
from mainapp.services.period_generator import period_generator


def menu(request) -> dict:
    """Возвращает список категорий статей"""

    categories = Category.objects.all()
    return {'categories': categories}


def top4(request) -> dict:
    """Возвращает словарь со списком из четырех самых рейтинговых пользователей"""

    top_four = get_most_rated()
    return {'most_rated_users': top_four}


def archive_peroids(request) -> dict:
    """Возращает словарь со списком временных интервалов Месяц-Год"""

    return {'periods': period_generator(request)}
