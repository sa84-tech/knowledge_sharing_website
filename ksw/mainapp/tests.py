from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from mainapp.models import Category, Post


class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_mainapp_urls(self):
        # проверка стнаницы помощи
        response = self.client.get('/help/')
        self.assertEqual(response.status_code, 200)

        # проверка главной страницы
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # проверка всех категорий
        for category in Category.objects.all():
            response = self.client.get(f'/category/{category.slug}')
            self.assertEqual(response.status_code, 200)

        # проверка всех статей
        for post in Post.objects.all():
            response = self.client.get(f'/post/{post.pk}')

        # проверка станицы логирования
        response = self.client.get('/auth/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp')
