from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, User, Post


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.small_img = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.jpg',
            content=cls.small_img,
            content_type='image/gif'
        )

        cls.group = Group.objects.create(
            title='Заголовок',
            description='Текст',
            slug='test-slug',
        )
        cls.user2 = User.objects.create_user(username='tester')
        cls.post = Post.objects.create(
            text='Проверочный текст',
            author=cls.user2,
            group=cls.group,
            image=cls.uploaded
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        pass

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='papavel')
        self.user2 = PostPagesTests.user2
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user2)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'index.html': reverse('posts:index'),
            'new_post.html': reverse('posts:new_post'),
            'group.html': (
                reverse('posts:group_posts', kwargs={'slug': 'test-slug'})
            ),
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_has_correct_context(self):
        """Провера контекста главной страницы,
           а также проверка на наличие одного-единственного
           поста на главной странице"""
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page']), 1)

        post = response.context['page'][0]
        self.assertEqual(post.text, PostPagesTests.post.text)
        self.assertEqual(post.author, PostPagesTests.post.author)
        self.assertEqual(post.group, PostPagesTests.post.group)
        self.assertEqual(post.image, PostPagesTests.post.image)

    def test_groups_page_has_correct_context(self):
        """Провера контекста страницы с записями сообщества"""
        response = self.authorized_client.get(reverse('posts:group_posts',
                                              kwargs={'slug': 'test-slug'}))
        group = response.context['group']
        post = response.context['page'][0]

        self.assertEqual(group.title, PostPagesTests.group.title)
        self.assertEqual(group.description, PostPagesTests.group.description)
        self.assertEqual(group.slug, PostPagesTests.group.slug)
        self.assertEqual(post.group.title, PostPagesTests.group.title)
        self.assertEqual(post.text, PostPagesTests.post.text)
        self.assertEqual(post.image, PostPagesTests.post.image)

    def test_new_post_has_correct_context(self):
        """Проверка контекста страницы создания новой записи"""
        response = self.authorized_client.get(reverse('posts:new_post'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_group_post_correct_deployment(self):
        """Проверка наличия записи на странице сообщества"""
        new_post = Post.objects.create(
            text='Текст1',
            author=User.objects.create_user(username='tester_man'),
            group=PostPagesTests.group
        )
        new_group = Group.objects.create(
            title='bad_group',
            description='bad description',
            slug='bad-slug'
        )
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertIn(new_post, response.context['page'])

        response = self.authorized_client.get(reverse('posts:group_posts',
                                              kwargs={'slug':
                                                      new_post.group.slug
                                                      }))
        self.assertIn(new_post, response.context['page'])

        response = self.authorized_client.get(reverse('posts:group_posts',
                                              kwargs={'slug': new_group.slug}))
        self.assertNotIn(new_post, response.context['page'])

    def test_edit_post_page_correct_context(self):
        """Проверка контекста страницы редактирования записи"""
        response = self.authorized_client2.get(reverse('posts:post_edit',
                                               kwargs={'username':
                                                       PostPagesTests.post.
                                                       author.username,
                                                       'post_id':
                                                       PostPagesTests.post.id
                                                       }))
        # Проверка формы
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields.get(value)
                self.assertIsInstance(form_field, expected)
        # Проверка поста
        post = response.context['post']
        self.assertEqual(post.text, PostPagesTests.post.text)
        self.assertEqual(post.group, PostPagesTests.post.group)
        self.assertEqual(post.author, PostPagesTests.post.author)

    def test_profile_page_has_correct_context(self):
        """Проверка контекста страницы с профайлом"""
        response = self.guest_client.get(reverse('posts:profile', kwargs={
                                         'username':
                                         PostPagesTests.post.author.username
                                         }))
        page = response.context['page']
        self.assertIn(PostPagesTests.post, page)
        author = response.context['author']
        self.assertEqual(self.user2, author)
        image = response.context['page'][0].image
        self.assertEqual(image, PostPagesTests.post.image)

    def test_specific_post_has_correct_context(self):
        """Проверка контекста страницы конкретной записи"""
        response = self.authorized_client2.get(reverse('posts:post', kwargs={
                                               'username':
                                               PostPagesTests.post.
                                               author.username,
                                               'post_id':
                                               PostPagesTests.post.id
                                               }))
        post = response.context['post']
        self.assertEqual(PostPagesTests.post, post)
        self.assertEqual(self.user2, post.author)

    def test_correct_404_redirect(self):
        """ Проверка: при срабатывании ошибки 404
            вызывается корректный шаблон"""
        response = self.client.get('/not_valid_url/')
        self.assertTemplateUsed(response, 'misc/404.html')

    def test_with_image_need_to_change_this_name(self):
        pass


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass

        cls.user = User.objects.create_user(username="Pavel")
        posts = [Post(author=cls.user,
                 text=f'Проверочный текст-{i}') for i in range(13)]
        Post.objects.bulk_create(posts)

    def setUp(self):
        self.client = Client()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass
        # Если убираю очистку данных - получаю
        # ERROR: setUpClass(posts.tests.test_views.PostPagesTests)
        Post.objects.all().delete()

    def test_first_page_containse_ten_records(self):
        """Проверка: количество постов на первой странице равно 10."""
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page'].object_list), 10)

    def test_second_page_containse_three_records(self):
        """Проверка: на второй странице должно быть три поста."""
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page'].object_list), 3)
