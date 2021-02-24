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
