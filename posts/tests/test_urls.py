from django.test import TestCase, Client

from posts.models import Post, Group, User


class PostUrlTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовое описание',
            slug='test-slug'
        )

        cls.templates_url_names = {
            '/': 'index.html',
            '/group/test-slug/': 'group.html',
            '/new/': 'new_post.html',
            '/Pavel/': 'profile.html',
            '/Pavel/1/': 'post.html',
            '/Pavel/1/edit/': 'new_post.html'
        }
        cls.pages_and_redirects = {
            '/new/': '/auth/login/?next=/new/',
            '/Pavel/1/edit/': '/auth/login/?next=/Pavel/1/edit/'
        }

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='Pavel')
        Post.objects.create(
            text="Тестовый текст",
            author=self.user
            # тут был id, как оказалось, я его не использолал :)
            # комментарий после ревью уберу
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_correct_template(self):
        for reverse_name, template in PostUrlTest.templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_urls_exists_at_desired_location(self):
        for reverse_name, template in PostUrlTest.templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertEquals(response.status_code, 200)

    def test_urls_redirects_anonymous_on_some_pages(self):
        for request, redirect_page in PostUrlTest.pages_and_redirects.items():
            with self.subTest():
                response = self.guest_client.get(request)
                self.assertRedirects(response, redirect_page)

    def test_visit_edit_post_page_by_author(self):
        response = self.authorized_client.get('/Pavel/1/edit/')
        self.assertEqual(response.status_code, 200)

    def test_visit_edit_post_page_by_authorized_user_but_not_author(self):
        user = User.objects.create(username='NotPavel')
        authorized_client = Client()
        authorized_client.force_login(user)
        response = authorized_client.get('/Pavel/1/edit/')
        self.assertRedirects(response, '/Pavel/1/')
