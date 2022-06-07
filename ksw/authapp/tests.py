from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command
from authapp.models import WriterUser

from mainapp.models import Post


class TestAuthappSmoke(TestCase):  # в .env DEBUG=False
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

        self.superuser = WriterUser.objects.create_superuser('super_test', 'super_django@test.local', '123test')
        self.user = WriterUser.objects.create_user('user1_test', 'user1_django@test.local', '123test')
        self.user_with__name = WriterUser.objects.create_user('user2_test', 'user2_django@test.local', '123test',
                                                              first_name='John', last_name='Dow', is_staff=True)

    def test_user_login(self):
        # доступность главной страницы для не авторизированного пользователя
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Главная страница')
        self.assertNotContains(response, f'@{self.user.username}', status_code=200)

        # данные пользователя
        self.client.login(username='user1_test', password='123test')

        # авторизируемся на сайте
        self.assertFalse(response.context['user'].is_active)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)
        self.assertTrue(response.context['user'].is_active)

        # доступность главной страницы для авторизированного пользователя
        response = self.client.get('/')
        self.assertContains(response, f'@{self.user.username}', status_code=200)
        self.assertEqual(response.context['user'], self.user)

        # доступность страницы помощи для авторизированного пользователя
        response = self.client.get('/help/')
        self.assertContains(response, f'@{self.user.username}', status_code=200)
        self.assertEqual(response.context['user'], self.user)

        # доступность админки для авторизированного пользователя
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)

        # доступность аккаунта для зарегистрированного пользователя
        response = self.client.get(f'/account/users/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

        for post in Post.objects.all():
            if post.status == "published":
                # доступность чужой опубликованной статьи для зарегистрированного пользователя
                response = self.client.get(f'/post/{post.pk}')
                self.assertEqual(response.status_code, 200)
            elif post.status == "draft":
                # доступность чужого "черновика" для зарегистрированного пользователя
                response = self.client.get(f'/post/{post.pk}')
                self.assertEqual(response.status_code, 404)
            elif post.status == 'under_review':
                # доступность чужой "статьи на модерации" для зарегистрированного пользователя
                response = self.client.get(f'/post/{post.pk}')
                self.assertEqual(response.status_code, 404)
            elif post.status == 'deleted':
                # доступность чужой "удаленной статьи" для зарегистрированного пользователя
                response = self.client.get(f'/post/{post.pk}')
                self.assertEqual(response.status_code, 404)

        self.client.logout()
        self.client.login(username='user2_test', password='123test')

        for post in Post.objects.all():
            # доступность чужой статьи для модератора
            if post.status == "draft":
                response = self.client.get(f'/post/{post.pk}')
                self.assertEqual(response.status_code, 200)
            elif post.status == 'under_review':
                response = self.client.get(f'/post/{post.pk}')
                self.assertEqual(response.status_code, 200)
            elif post.status == 'deleted':
                response = self.client.get(f'/post/{post.pk}')
                self.assertEqual(response.status_code, 404)

        self.client.logout()

        # доступность админки для не зарегистрированного пользователя
        response = self.client.get('/admin/')
        self.assertNotEqual(response.status_code, 200)
        # доступность аккаунта для не зарегистрированного пользователя
        response = self.client.get(f'/account/users/{self.user.username}/')
        self.assertNotEqual(response.status_code, 200)


    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp')
