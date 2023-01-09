from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    titlemaxlenght = 200

    title = models.CharField('заголовок', max_length=titlemaxlenght)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание')

    def __str__(self) -> models.CharField:
        return self.title


class Post(models.Model):
    text = models.TextField('текст поста', help_text='Текст нового поста')
    pub_date = models.DateTimeField('время публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='группа',
        help_text='Группа, к которой будет относиться пост'
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'posts'

    def __str__(self) -> str:
        return self.text[:15]  # первые 15 символов поста
