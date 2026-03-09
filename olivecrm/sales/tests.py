from django.test import TestCase
from olivecrm.contacts.models import Contact
from .models import Pipeline, Deal, Task

class SalesModelTest(TestCase):
    def setUp(self):
        self.pipeline = Pipeline.objects.create(name="Standard Sales", is_default=True)
        self.contact = Contact.objects.create(first_name="Buyer", last_name="Doe")
        self.deal = Deal.objects.create(
            name="Cloud Project",
            pipeline=self.pipeline,
            contact=self.contact,
            amount=50000,
            stage="discovery",
            stage_order=1
        )
        from django.utils import timezone
        self.task = Task.objects.create(
            title="Follow up call",
            deal=self.deal,
            priority="high",
            status="todo",
            due_date=timezone.now()
        )

    def test_deal_stage(self):
        self.assertEqual(self.deal.stage, "discovery")
        self.assertEqual(self.deal.amount, 50000)

    def test_task_assignment(self):
        self.assertEqual(self.task.deal.name, "Cloud Project")
        self.assertEqual(self.task.priority, "high")
