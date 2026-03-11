from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ReportViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', password='test'
        )
        self.client.login(username='test', password='test')

    def test_index_loads(self):
        r = self.client.get(reverse('reporting:index'))
        self.assertEqual(r.status_code, 200)

    def test_sales_tab_loads(self):
        r = self.client.get(reverse('reporting:sales') + '?period=month')
        self.assertEqual(r.status_code, 200)

    def test_revenue_tab_loads(self):
        r = self.client.get(reverse('reporting:revenue') + '?period=month')
        self.assertEqual(r.status_code, 200)

    def test_contacts_tab_loads(self):
        r = self.client.get(reverse('reporting:contacts') + '?period=month')
        self.assertEqual(r.status_code, 200)

    def test_performance_tab_loads(self):
        r = self.client.get(reverse('reporting:performance') + '?period=month')
        self.assertEqual(r.status_code, 200)

    def test_export_sales_csv(self):
        r = self.client.get(reverse('reporting:export_sales'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'text/csv')

    def test_export_revenue_csv(self):
        r = self.client.get(reverse('reporting:export_revenue'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'text/csv')

    def test_export_contacts_csv(self):
        r = self.client.get(reverse('reporting:export_contacts'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r['Content-Type'], 'text/csv')
