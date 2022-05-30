from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from mainapp.models import Category


class TestMainappSmoke(TestCase):  # в .env DEBUG=False
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'init_data.json')
        self.client = Client()

    def test_mainapp_urls(self):

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        for category in Category.objects.all():
            response = self.client.get(f'/{category.slug}')
            self.assertEqual(response.status_code, 200)

