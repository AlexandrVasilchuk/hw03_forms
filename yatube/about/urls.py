from django.urls import path

from about import apps, views

app_name = apps.AboutConfig.name

urlpatterns = [
    path('author/', views.AboutAuthorView.as_view(), name='author'),
    path('tech/', views.AboutTechView.as_view(), name='tech'),
]
