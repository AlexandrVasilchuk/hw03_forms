from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
User = get_user_model()


class TestUsersViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(TestUsersViews.user)

    def test_correct_templates(self):
        response_expected = {
            reverse(
                'users:password_change_form'
            ): 'users/password_change.html',
            reverse(
                'users:password_change_done'
            ): 'users/password_change_done.html',
            reverse(
                'users:password_reset_form'
            ): 'users/password_reset_form.html',
            reverse(
                'users:password_reset_complete'
            ): 'users/password_reset_complete.html',
            reverse(
                'users:password_reset_done'
            ): 'users/password_reset_done.html',
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': 'MQ', 'token': '67t-0041e063fc003f28187f'},
            ): 'users/password_reset_confirm.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:logout'): 'users/logged_out.html',
        }
        for response, expected in response_expected.items():
            with self.subTest(expected=expected):
                self.assertTemplateUsed(
                    self.authorized_client.get(response),
                    expected,
                    msg_prefix=f'Ошибка, ожидался шаблон {expected}',
                )

    def test_correct_context(self):
        """Проверка правильности контекста для signup"""
        response = self.authorized_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
        }
        for value, expected in form_fields.items():
            with self.subTest(field=value):
                self.assertIsInstance(response.context['form'].fields[value], expected)
