import json
import os
from getpass import getpass

from django.core.management import BaseCommand
import environ

from ksw.settings import BASE_DIR
from mainapp.models import StatusArticle, Category
from authapp.models import WriterUser

env = environ.Env()
environ.Env.read_env()

try:
    ADM_PASSWD = env('INIT_ADM_PSWD')
except environ.ImproperlyConfigured:
    ADM_PASSWD = getpass('Введите пароль для Администратора: ')


class Command(BaseCommand):
    def handle(self, *args, **options):

        if not WriterUser.objects.filter(is_superuser=True):
            super_user = WriterUser.objects.create_superuser(
                'admin', 'admin@example.com', ADM_PASSWD)
            print(f'** user created ** ({super_user})')

        try:
            file_path = os.path.join(BASE_DIR, 'ksw', 'init_data.json')
            with open(file_path, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)

            if data.get('statuses'):
                for status in data['statuses']:
                    self.print_creation_result(*StatusArticle.objects.get_or_create(**status))

            if data.get('categories'):
                for category in data['categories']:
                    self.print_creation_result(*Category.objects.get_or_create(**category))

        except IOError:
            print(str(IOError))
            return

    def print_creation_result(self, obj: object, is_created: bool = None):
        if is_created:
            print(f'** New {type(obj).__name__} with id {obj.id} created **')
        else:
            print(f'** {type(obj).__name__} with id {obj.id} already exists **')
