from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from authapp.models import WriterUser


class TestAuthappSmoke(TestCase):  # в .env DEBUG=False
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = WriterUser.objects.create_superuser('super_test', 'super_django@test.local', '123test')
        self.user = WriterUser.objects.create_user('user1_test', 'user1_django@test.local', '123test')
        self.user_with__name = WriterUser.objects.create_user('user2_test', 'user2_django@test.local', '123test',
                                                              first_name='John', last_name='Dow')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Главная страница')
        self.assertNotContains(response, f'@{self.user.username}', status_code=200)

        self.client.login(username='user1_test', password='123test')

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        response = self.client.get('/')
        self.assertContains(response, f'@{self.user.username}', status_code=200)
        self.assertEqual(response.context['user'], self.user)


    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp')
