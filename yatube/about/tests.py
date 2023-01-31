from http import HTTPStatus
from django.urls import reverse
from django.test import Client, TestCase


class StaticPagesTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_urls(self):
        """Проверка доступности страниц приложения about"""
        response_values = {
            '/about/author/': HTTPStatus.OK,
            '/about/tech/': HTTPStatus.OK,
        }
        for value, expected in response_values.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.guest_client.get(value).status_code,
                    expected,
                    f'Страница {value} недоступна по нужному адресу!',
                )


class StaticPagesViewsTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_views(self):
        """Проверка использования верных шаблонов"""
        response_values = {
            'about:author': 'about/about.html',
            'about:tech': 'about/tech.html'
        }
        for response, expected in response_values.items():
            with self.subTest(expected=expected):
                self.assertTemplateUsed(self.guest_client.get(reverse(response)), expected)