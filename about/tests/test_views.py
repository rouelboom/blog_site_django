from django.test import Client, TestCase
from django.urls import reverse


class AboutPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.template_names = {
            'about:author': 'about/about.html',
        }

    def setUp(self):
        self.guest_client = Client()

    def test_about_page_accessible_by_name(self):
        """URLы, генерируемые при помощи имени about, доступны."""
        for value, expected in AboutPagesTests.template_names.items():
            with self.subTest(value=value):
                response = self.guest_client.get(reverse(value))
                self.assertEqual(response.status_code, 200)

    def test_about_page_uses_correct_template(self):
        """При запросе к именам about
        применяется корректный шаблон."""
        for value, expected in AboutPagesTests.template_names.items():
            with self.subTest(value=value):
                response = self.guest_client.get(reverse(value))
                self.assertTemplateUsed(response, expected)
