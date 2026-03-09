from django.test import TestCase
from django.contrib.auth.models import User
from .models import EmailAccount, WhatsAppMessage
from olivecrm.contacts.models import Contact

class CommunicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="comm_user", password="password")
        self.account = EmailAccount.objects.create(
            user=self.user,
            email_address="comm@example.com",
            imap_server="imap.example.com",
            username="comm@example.com",
            password="securepassword"
        )
        self.contact = Contact.objects.create(first_name="WhatsApp", last_name="User")
        self.whatsapp = WhatsAppMessage.objects.create(
            contact=self.contact,
            message_id="msg_123",
            direction="outbound",
            content="Hello from OliveCRM"
        )

    def test_email_account_creation(self):
        self.assertEqual(self.account.email_address, "comm@example.com")
        self.assertEqual(self.account.user.username, "comm_user")

    def test_whatsapp_message(self):
        self.assertEqual(self.whatsapp.contact.first_name, "WhatsApp")
        self.assertEqual(self.whatsapp.direction, "outbound")
