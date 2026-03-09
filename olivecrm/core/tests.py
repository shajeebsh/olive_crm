from django.test import TestCase
from unittest.mock import MagicMock, patch
from .ai_service import AIService
from .models import AuditLog
from django.contrib.auth.models import User

class AIServiceTest(TestCase):
    def setUp(self):
        self.ai_service = AIService()

    @patch('openai.OpenAI')
    def test_score_lead_mock(self, mock_openai):
        # Setup mock
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content=" 85 "))]
        mock_client.chat.completions.create.return_value = mock_response
        
        self.ai_service.client = mock_client
        
        score = self.ai_service.score_lead({"title": "CEO", "company_size": "500"})
        self.assertEqual(score, 85)

class AuditLogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="auditor", password="password")
        self.log = AuditLog.objects.create(
            user=self.user,
            action="update",
            object_type="Contact",
            object_id="1",
            changes={"status": ["new", "hot"]}
        )

    def test_log_creation(self):
        self.assertEqual(self.log.action, "update")
        self.assertEqual(self.log.user.username, "auditor")
