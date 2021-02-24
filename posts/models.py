from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):

    title = models.CharField("Название группы", max_length=200)
    slug = models.SlugField("Читабельный адрес группы", unique=True,
                            blank=True, null=True)
    description = models.TextField("Описание группы", default='')

    class Meta:
        verbose_name = "Сообщество"
        verbose_name_plural = "Сообщества"

    def __str__(self):
        return self.title


class Post(models.Model):

    text = models.TextField("Ваша запись",
                            help_text="Поле обязательно для заполнения")

    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="posts",
                               verbose_name="Автор записи")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL,
                              related_name="posts",
                              verbose_name="Сообщество",
                              blank=True, null=True,
                              help_text="Запись может не иметь сообщества")

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='follower',
                             verbose_name='Подписчик',
                             on_delete=models.SET_NULL)
    author = models.ForeignKey(User, related_name='following',
                               verbose_name='Автор',
                               on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.text[:15]