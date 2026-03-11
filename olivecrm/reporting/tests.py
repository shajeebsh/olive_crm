from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ReportsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_reports_index_loads(self):
        response = self.client.get(reverse('reporting:index'))
        self.assertEqual(response.status_code, 200)
