import json
import os
from random import getrandbits

from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.db import IntegrityError
import environ

from ksw.settings import BASE_DIR
from mainapp.models import StatusArticle, Category, Post, Comment
from authapp.models import WriterUser
from accountapp.models import Bookmark

env = environ.Env()
environ.Env.read_env()
ADM_PASSWD = env('INIT_ADM_PSWD')
USR_PASSWD = env('INIT_USRS_PSWD')


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
                    self.save(*StatusArticle.objects.get_or_create(**status))

            if data.get('categories'):
                for category in data['categories']:
                    self.save(*Category.objects.get_or_create(**category))

            if data.get('posts'):
                for post in data['posts']:
                    post['category'] = Category.objects.get(pk=post['category'])
                    post['status'] = StatusArticle.objects.get(pk=post['status'])
                    post['author'] = WriterUser.objects.get(username=post['author'])
                    self.save(*Post.objects.get_or_create(**post))

            if data.get('comments'):
                for comment in data['comments']:
                    comment['content_type'] = ContentType.objects.get(model=comment['content_type_name'])
                    del comment['content_type_name']
                    self.save(*Comment.objects.get_or_create(**comment))

            # Create bookmarks for random posts and comments
            for user in WriterUser.objects.all():
                target_types = [Post, Comment]
                for target_type in target_types:
                    content_type = ContentType.objects.get_for_models(target_type)[target_type]
                    bookmark = {'author': user, 'content_type': content_type}
                    for obj in target_type.objects.all():
                        if bool(getrandbits(1)):
                            continue
                        bookmark['object_id'] = obj.id
                        self.save(*Bookmark.objects.get_or_create(**bookmark))

        except IOError:
            print(str(IOError))
            return

    def save(self, obj, is_created=None):
        if is_created:
            obj.save()
            print(f'** New {type(obj).__name__} with id {obj.id} created **')
        else:
            print(f'** {type(obj).__name__} with id {obj.id} already exists **')
