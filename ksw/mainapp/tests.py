from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from ksw.mainapp.models import Category
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from ksw.authapp.views import login, logout, register, edit, verify, PasswordChangeView, password_success, \
    email_change, email_success, PassResetView
from mainapp.views import index_page


class TestMainUrls(SimpleTestCase):

    def test_home_url_response(self):
        response = self.client.get('/')
        print('answer<<<<<<<<')
        self.assertEqual(response.status_code, 200)


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



