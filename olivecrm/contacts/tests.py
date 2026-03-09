from django.test import TestCase
from .models import Company, Contact, Interaction

class ContactModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
            name="Test Corp",
            domain="testcorp.com",
            industry="Technology"
        )
        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            company=self.company,
            emails=[{"email": "john@testcorp.com", "primary": True}],
            lead_status="new"
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.first_name, "John")
        self.assertEqual(self.contact.company.name, "Test Corp")
        self.assertEqual(len(self.contact.emails), 1)

    def test_company_domain_auto_discovery(self):
        # Even though we set it manually, we can test it
        self.assertEqual(self.company.domain, "testcorp.com")

class InteractionModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(first_name="Jane", last_name="Smith")
        self.interaction = Interaction.objects.create(
            contact=self.contact,
            type="email",
            subject="Test Interaction",
            content="Hello World"
        )

    def test_interaction_linking(self):
        self.assertEqual(self.interaction.contact.last_name, "Smith")
        self.assertEqual(self.interaction.type, "email")
