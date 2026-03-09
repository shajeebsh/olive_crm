from django.test import TestCase
from olivecrm.contacts.models import Contact
from .models import MailingList, EmailCampaign

class MarketingModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(first_name="Member", last_name="One")
        self.mailing_list = MailingList.objects.create(name="Hot Leads")
        self.mailing_list.contacts.add(self.contact)
        self.campaign = EmailCampaign.objects.create(
            name="Spring Sale",
            subject="Exclusive Offer",
            target_list=self.mailing_list
        )

    def test_campaign_targeting(self):
        self.assertEqual(self.campaign.target_list.name, "Hot Leads")
        self.assertEqual(self.campaign.target_list.contacts.count(), 1)
