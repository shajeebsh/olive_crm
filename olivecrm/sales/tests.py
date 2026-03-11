from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class SalesViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_pipeline_kanban_loads(self):
        response = self.client.get(reverse('pipeline:pipeline_kanban'))
        self.assertEqual(response.status_code, 200)
