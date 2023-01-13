from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD
    name = 'core'
    verbose_name = 'ядро'
