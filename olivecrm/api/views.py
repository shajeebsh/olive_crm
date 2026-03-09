from rest_framework import viewsets
from olivecrm.contacts.models import Contact, Company
from olivecrm.sales.models import Deal
from olivecrm.invoicing.models import Invoice
from olivecrm.inventory.models import Product
from .serializers import (
    ContactSerializer, CompanySerializer, DealSerializer, 
    InvoiceSerializer, ProductSerializer
)

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
