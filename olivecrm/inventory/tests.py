from django.test import TestCase
from .models import Product, Warehouse, StockLevel

class InventoryModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Widget", sku="W-001", price=10)
        self.warehouse = Warehouse.objects.create(name="Main Hub")
        self.stock = StockLevel.objects.create(
            product=self.product,
            warehouse=self.warehouse,
            quantity=100
        )

    def test_stock_level(self):
        self.assertEqual(self.stock.quantity, 100)
        self.assertEqual(self.stock.product.sku, "W-001")
