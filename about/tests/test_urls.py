from django.test import Client, TestCase


class AboutURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template_names = {
            '/about/author/': 'about/about.html',
        }

    def setUp(self):
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адресов /about/xxx."""
        for value, template in AboutURLTests.template_names.items():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
                self.assertEqual(response.status_code, 200)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /about/."""
        for value, template in AboutURLTests.template_names.items():
            with self.subTest(value=value):
                response = self.guest_client.get(value)
        response = self.guest_client.get(value)
        self.assertTemplateUsed(response, template)
