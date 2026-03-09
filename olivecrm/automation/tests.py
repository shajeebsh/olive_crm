from django.test import TestCase
from .models import Workflow
from django.contrib.auth.models import User

class AutomationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="workflow_admin", password="password")
        self.workflow = Workflow.objects.create(
            name="Warm Lead Welcome",
            trigger_type="record_created",
            trigger_config={"object_type": "Contact"},
            actions=[{"type": "send_email", "template": "welcome"}],
            created_by=self.user
        )

    def test_workflow_creation(self):
        self.assertEqual(self.workflow.name, "Warm Lead Welcome")
        self.assertEqual(len(self.workflow.actions), 1)
        self.assertTrue(self.workflow.is_active)
