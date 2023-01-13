from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path, reverse_lazy

from users import apps, views

app_name = apps.UsersConfig.name
passwords = [
    path(
        'change/form',
        PasswordChangeView.as_view(
            success_url=reverse_lazy('users:password_change_done'),
            template_name='users/password_change.html',
        ),
        name='password_change_form',
    ),
    path(
        'change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'reset/form',
        PasswordResetView.as_view(
            success_url=reverse_lazy('users:password_reset_done'),
            template_name='users/password_reset_form.html',
        ),
        name='password_reset_form',
    ),
    path(
        'reset/complete',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete',
    ),
    path(
        'reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:password_reset_complete'),
            template_name='users/password_reset_confirm.html',
        ),
        name='password_reset_confirm',
    ),
]
urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout',
    ),
    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup',
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login',
    ),
    path('password/', include(passwords)),
]
