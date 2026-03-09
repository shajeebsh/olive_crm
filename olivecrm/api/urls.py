from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactViewSet, CompanyViewSet, DealViewSet, 
    InvoiceViewSet, ProductViewSet
)

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'deals', DealViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
