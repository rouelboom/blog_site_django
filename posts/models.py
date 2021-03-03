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
    image = models.ImageField("Изображение",
                              upload_to='posts/',
                              blank=True, null=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments",
                             verbose_name="Комментарий",
                             help_text="Комментарии к этому посту")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="comments",
                               verbose_name="Автор комментария",
                               help_text="Комментарий автора")
    text = models.TextField("Текст комментария",
                            help_text="Поле обязательно для заполнения")
    created = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class Follow(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower",
                             verbose_name="Подписчик",
                             help_text="Он подписывается")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following",
                               verbose_name="Автор",
                               help_text="На него подписываются")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=("user", "author"), name="no_twice")
        ]

    def __str__(self):
        return f"{self.user} является подписчиков {self.author}"
