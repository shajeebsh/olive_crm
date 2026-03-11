from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class SettingsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_settings_index_loads(self):
        # Settings namespace uses core.urls
        response = self.client.get(reverse('settings:index'))
        self.assertEqual(response.status_code, 200)
