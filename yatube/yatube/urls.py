from django.contrib import admin
from django.urls import include, path

from about.apps import AboutConfig
from posts.apps import PostsConfig
from users.apps import UsersConfig

urlpatterns = [
    path('auth/', include('users.urls', namespace=UsersConfig.name)),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('posts.urls', namespace=PostsConfig.name)),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls', namespace=AboutConfig.name)),
]
