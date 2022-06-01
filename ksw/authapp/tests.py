from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from authapp.models import WriterUser



class TestAuthappSmoke(TestCase):  # в .env DEBUG=False
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'init_data.json')
        self.client = Client()

        self.superuser = WriterUser.objects.create_superuser('super_test', 'super_django@test.local', '123test')
        self.superuser = WriterUser.objects.create_user('user1_test', 'user1_django@test.local', '123test')
        self.superuser = WriterUser.objects.create_user('user2_test', 'user2_django@test.local', '123test',
                                                        first_name='user2')

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Главная')
