from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=PostURLTest.user,
            group=PostURLTest.group,
            text='Тестовый пост более 15 символов',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(PostURLTest.user)

    def test_exists_at_desired_location(self):
        """Проверка доступности страниц по указанным адресам для всех"""
        response_values = {
            self.guest_client.get(''): HTTPStatus.OK,
            self.guest_client.get('/group/test_group_slug/'): HTTPStatus.OK,
            self.guest_client.get('/profile/auth/'): HTTPStatus.OK,
            self.guest_client.get(
                f'/posts/{PostURLTest.post.pk}/'
            ): HTTPStatus.OK,
        }
        for value, expected in response_values.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value.status_code,
                    expected,
                    'Страница не доступна всем по нужному адресу!',
                )

    def test_redirect_for_anonymous(self):
        """Проверка редиректа анонимного пользователя"""
        response_values = {
            self.guest_client.get(
                '/create/', follow=True
            ): '/auth/login/?next=/create/',
            self.guest_client.get(
                f'/posts/{PostURLTest.post.pk}/edit/', follow=True
            ): f'/auth/login/?next=/posts/{PostURLTest.post.pk}/edit/',
        }
        for value, expected in response_values.items():
            with self.subTest(value=value):
                self.assertRedirects(
                    value,
                    expected,
                    msg_prefix='Редирект работает неправильно!',
                )

    def test_available_authorized_users(self):
        """Проверка доступности страницы для авторизованного"""
        response_values = {
            self.authorized_client.get('/create/'): HTTPStatus.OK,
        }
        for value, expected in response_values.items():
            with self.subTest(value=value):
                self.assertEqual(
                    value.status_code,
                    expected,
                    'Страницы недоступны авторизованным пользователям!',
                )

    def test_author_available(self):
        response = self.authorized_client.get(
            f'/posts/{PostURLTest.post.pk}/edit/'
        )
        value = HTTPStatus.OK
        self.assertEqual(response.status_code, value)

    def test_not_author_available(self):
        self.not_author = User.objects.create_user(username='_')
        self.authorized_client.force_login(self.not_author)
        response = self.authorized_client.get(
            f'/posts/{PostURLTest.post.pk}/edit/'
        )
        value = f'/posts/{PostURLTest.post.pk}/'
        self.assertRedirects(response, value)

    def test_is_template_available(self):
        response_values = {
            '': 'posts/index.html',
            '/create/': 'posts/create_post.html',
            '/group/test_group_slug/': 'posts/group_list.html',
            f'/posts/{PostURLTest.post.pk}/': 'posts/post_detail.html',
            f'/posts/{PostURLTest.post.pk}/edit/': 'posts/create_post.html',
            f'/profile/auth/': 'posts/profile.html',
        }
        for response, value in response_values.items():
            with self.subTest(value=value):
                self.assertTemplateUsed(
                    self.authorized_client.get(response),
                    value,
                    f'Открывается неверный шаблон по ссылке {response}!',
                )
