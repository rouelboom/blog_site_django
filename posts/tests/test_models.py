from django.test import TestCase

from posts.models import Post, Group, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.example = Post.objects.create(
            author=User.objects.create_user(username="tester"),
            text="looooong text - 123456789",
        )

    def test_readable_verbose_name(self):
        data = PostModelTest.example
        field_verboses = {
            "text": "Ваша запись",
            "pub_date": "Дата публикации",
            "group": "Сообщество",
            "author": "Автор записи"
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEquals(data._meta.get_field(value).verbose_name,
                                  expected)

    def test_str_method(self):
        data = PostModelTest.example
        self.assertEquals(data.text[:15], str(data))


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.example = Group.objects.create(
            title="Победители",
            slug="winners",
            description="Хорошие ребята"
        )

    def test_readable_verbose_name(self):
        data = GroupModelTest.example
        field_verboses = {
            "title": "Название группы",
            "slug": "Читабельный адрес группы",
            "description": "Описание группы",
        }

        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEquals(data._meta.get_field(value).verbose_name,
                                  expected)

    def test_str_method(self):
        data = GroupModelTest.example
        self.assertEquals(data.title, str(data))
