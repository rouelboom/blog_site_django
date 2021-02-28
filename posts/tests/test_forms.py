import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class FormsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Описание тестовой группы'
        )
        cls.user = User.objects.create_user(username='tester')
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_new_post_by_anonimous(self):
        """ Попытка создать новую запись анонимным пользователем """
        response = self.guest_client.get(reverse('posts:new_post'))
        login = reverse('login')
        next_redirect = reverse('posts:new_post')
        url = f'{login}?next={next_redirect}'
        self.assertRedirects(response, url)

    def test_cant_create_post_without_text(self):
        """ Попытка создать пост с невалидной формой"""
        posts_count = Post.objects.count()
        form_data = {
            'text': ''
        }
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertFormError(
            response, 'form', 'text', 'Обязательное поле.'
        )
        self.assertEqual(response.status_code, 200)

    def test_post_creation(self):
        """ Попытка создания валидного поста """
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Пост c группой',
            'group': FormsPagesTests.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Пост c группой',
                                            group=FormsPagesTests.
                                            group).exists())

    def test_post_creation_with_image(self):
        """ Попытка создания валидного поста с картинкой"""
        small_img = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.jpg',
            content=small_img,
            content_type='image/gif'
        )
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Пост c группой',
            'group': FormsPagesTests.group.id,
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:new_post'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(text='Пост c группой').exists())
