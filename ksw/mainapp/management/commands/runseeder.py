import json
import os
from getpass import getpass
from random import getrandbits

from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db import IntegrityError
import environ

from ksw.settings import BASE_DIR
from mainapp.models import StatusArticle, Category, Post, Comment, View, Like
from authapp.models import WriterUser
from accountapp.models import Bookmark

env = environ.Env()
environ.Env.read_env()

try:
    ADM_PASSWD = env('INIT_ADM_PSWD')
except environ.ImproperlyConfigured:
    ADM_PASSWD = getpass('Введите пароль для администратора: ')

try:
    USR_PASSWD = env('INIT_USRS_PSWD')
except environ.ImproperlyConfigured:
    USR_PASSWD = getpass('Введите пароль для пользователей: ')


class Command(BaseCommand):
    def handle(self, *args, **options):

        if not WriterUser.objects.filter(is_superuser=True):
            super_user = WriterUser.objects.create_superuser(
                'admin', 'admin@example.com', ADM_PASSWD, first_name='Иван', last_name='Птичкин')
            print(f'** user created ** ({super_user})')

        try:
            file_path = os.path.join(BASE_DIR, 'ksw', 'init_data.json')
            with open(file_path, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)

            if data.get('users'):
                for user in data['users']:
                    try:
                        new_user = WriterUser.objects.create_user(**user, password=USR_PASSWD)
                        new_user.save()
                        print(f'** New User Created ({new_user.username}) **')
                    except IntegrityError:
                        print(f'** User Already Exists **')

            if data.get('statuses'):
                for status in data['statuses']:
                    self.print_creation_result(*StatusArticle.objects.get_or_create(**status))

            if data.get('categories'):
                for category in data['categories']:
                    self.print_creation_result(*Category.objects.get_or_create(**category))

            if data.get('posts'):
                for post in data['posts']:
                    post['category'] = Category.objects.get(pk=post['category'])
                    post['status'] = StatusArticle.objects.get(pk=post['status'])
                    post['author'] = WriterUser.objects.get(username=post['author'])
                    self.print_creation_result(*Post.objects.get_or_create(**post))

            if data.get('comments'):
                for comment in data['comments']:
                    comment['content_type'] = ContentType.objects.get(model=comment['content_type_name'])
                    del comment['content_type_name']
                    self.print_creation_result(*Comment.objects.get_or_create(**comment))

            # Create views, bookmarks and likes for random posts and comments
            bookmarks = []
            likes = []
            views = []
            for user in WriterUser.objects.all():
                target_types = [Post, Comment]
                for target_type in target_types:
                    content_type = ContentType.objects.get_for_model(target_type)
                    bookmark = {'author': user, 'content_type': content_type}
                    like = {'author': user, 'content_type': content_type}
                    view = {'author': user, 'content_type': content_type}
                    for obj in target_type.objects.all():
                        if bool(getrandbits(1)):
                            bookmark['object_id'] = obj.id
                            bookmarks.append(Bookmark(**bookmark))
                        if bool(getrandbits(1)):
                            like['object_id'] = obj.id
                            likes.append(Like(**like))
                        if target_type == Post and bool(getrandbits(1)):
                            view['object_id'] = obj.id
                            views.append(View(**view))

            for obj_list in views, bookmarks, likes:
                self.bulk_save_objects(obj_list)
                del obj_list

        except IOError:
            print(str(IOError))
            return

    def print_creation_result(self, obj: object, is_created: bool = None):
        if is_created:
            print(f'** New {type(obj).__name__} with id {obj.id} created **')
        else:
            print(f'** {type(obj).__name__} with id {obj.id} already exists **')

    def bulk_save_objects(self, objects: list):
        obj_model = type(objects[0])
        obj_model.objects.bulk_create(objects, ignore_conflicts=True)
        print(f'{len(objects)} objects for model {obj_model.__name__} created.')
