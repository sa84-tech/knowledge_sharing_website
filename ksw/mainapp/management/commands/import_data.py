import json
import os
from datetime import datetime, timedelta, timezone
from random import randint
from django.core.management import BaseCommand
import environ
from ksw.ksw.settings import BASE_DIR
from django.contrib.auth.models import User
from django.db import IntegrityError
from ksw.mainapp.models import StatusArticle, Category, Post


env = environ.Env()
environ.Env.read_env()
ADM_PASSWD = env('INIT_ADM_PSWD')
USR_PASSWD = env('INIT_USRS_PSWD')


class Command(BaseCommand):
    def handle(self, *args, **options):

        if not User.objects.filter(is_superuser=True):
            super_user = User.objects.create_superuser('admin', 'admin@example.com', ADM_PASSWD)
            print(f'** user created ** ({super_user})')

        try:
            file_path = os.path.join(BASE_DIR, 'ksw', 'init_data.json')
            with open(file_path, 'r', encoding='utf-8') as read_file:
                data = json.load(read_file)

            if data.get('users'):
                for user in data['users']:
                    try:
                        new_user = User.objects.create_user(**user, password=USR_PASSWD)
                        new_user.save()
                        print(f'** New User Created ({new_user.username}) **')
                    except IntegrityError:
                        print(f'** User Already Exists **')

            if data.get('statuses'):
                for status in data['statuses']:
                    new_status, is_created = StatusArticle.objects.get_or_create(**status)
                    if is_created:
                        new_status.save()
                        print(f'** New Status Created ({new_status.name}) **')
                    else:
                        print(f'** Status Already Exists **')

            if data.get('categories'):
                for category in data['categories']:
                    new_category, is_created = Category.objects.get_or_create(**category)
                    if is_created:
                        new_category.save()
                        print(f'** New Category Created ({new_category.name}) **')
                    else:
                        print(f'** Category Already Exists **')

            if data.get('posts'):
                for post in data['posts']:
                    post['category'] = Category.objects.get(pk=post['category'])
                    post['status'] = StatusArticle.objects.get(pk=post['status'])
                    post['author'] = User.objects.get(username=post['author'])
                    new_post, is_created = Post.objects.get_or_create(**post)
                    if is_created:
                        new_post.save()
                        print(f'** New Post Created ({new_post.topic}) **')
                    else:
                        print(f'** Post Already Exists **')

        except IOError:
            print(str(IOError))
            return
