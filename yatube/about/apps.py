from django.apps import AppConfig
from django.conf import settings


class AboutConfig(AppConfig):
    default_auto_field = settings.DEFAULT_AUTO_FIELD
    name = 'about'
    verbose_name = 'подробнее'
