from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Warehouse, Goods, Inventory


class InventoryAPITestCase(APITestCase):
    def setUp(self):
        self.warehouse = Warehouse.objects.create(name="Warehouse A", location="Location A")
        self.goods = Goods.objects.create(sku="SKU123", name="Test Goods", description="Test Description")
        self.inventory = Inventory.objects.create(warehouse=self.warehouse, goods=self.goods, quantity=50)

    def test_create_inventory(self):
        data = {
            "warehouse_id": self.warehouse.id,
            "goods_id": self.goods.id,
            "quantity": 100
        }
        response = self.client.post("/api/inventory/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["quantity"], 100)

    def test_update_inventory(self):
        data = {
            "warehouse_id": self.warehouse.id,
            "goods_id": self.goods.id,
            "quantity": 20,
            "action": "deduct"
        }
        response = self.client.post("/api/inventory/update/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["quantity"], 30)

    def test_delete_inventory(self):
        response = self.client.delete(f"/api/inventory/delete/{self.inventory.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Inventory.objects.filter(id=self.inventory.id).exists())