from django.test import TestCase
from olivecrm.contacts.models import Contact
from .models import Invoice, LineItem, Payment

class InvoicingModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(first_name="Invoice", last_name="User")
        self.invoice = Invoice.objects.create(
            number="INV-001",
            contact=self.contact,
            issue_date="2026-03-01",
            due_date="2026-03-15"
        )

    def test_invoice_totals(self):
        item1 = LineItem.objects.create(
            invoice=self.invoice,
            description="Consulting",
            quantity=10,
            unit_price=100,
            total=1000
        )
        # Total should be 1000 subtotal + 100 tax (10%) = 1100
        self.invoice.refresh_from_db()
        self.assertEqual(float(self.invoice.subtotal), 1000.0)
        self.assertEqual(float(self.invoice.total_amount), 1100.0)

    def test_payment_updates_status(self):
        LineItem.objects.create(
            invoice=self.invoice,
            description="Service",
            quantity=1,
            unit_price=100,
            total=100
        )
        self.invoice.refresh_from_db() # total 110
        
        Payment.objects.create(
            invoice=self.invoice,
            amount=110,
            payment_date="2026-03-02",
            payment_method="Bank"
        )
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'paid')
        self.assertEqual(float(self.invoice.amount_paid), 110.0)
