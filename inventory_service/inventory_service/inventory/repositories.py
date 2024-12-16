from .models import Warehouse, Goods, Inventory
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


class WarehouseRepository:
    def get_all(self):
        return Warehouse.objects.all()

    def get_by_id(self, warehouse_id):
        try:
            return Warehouse.objects.get(id=warehouse_id)
        except ObjectDoesNotExist:
            return None

    def create(self, name, location):
        return Warehouse.objects.create(name=name, location=location)

    # Additional methods as needed
    def update(self, warehouse_id, name, location):
        warehouse = self.get_by_id(warehouse_id)
        if warehouse:
            warehouse.name = name
            warehouse.location = location
            warehouse.save()
        return warehouse

    def delete(self, warehouse_id):
        warehouse = self.get_by_id(warehouse_id)
        if warehouse:
            warehouse.delete()


class GoodsRepository:
    def get_all(self):
        return Goods.objects.all()

    def get_by_id(self, goods_id):
        try:
             return Goods.objects.get(id=goods_id)
        except ObjectDoesNotExist:
            return None

    def get_by_sku(self, sku):
        try:
            return Goods.objects.get(sku=sku)
        except ObjectDoesNotExist:
            return None

    def create(self, sku, name, description=None):
        return Goods.objects.create(sku=sku, name=name, description=description)

    # Additional methods as needed
    def update(self, goods_id, sku, name, description):
        goods = self.get_by_id(goods_id)
        if goods:
            goods.sku = sku
            goods.name = name
            goods.description = description
            goods.save()
        return goods

    def delete(self, goods_id):
         goods = self.get_by_id(goods_id)
         if goods:
            goods.delete()


class InventoryRepository:
    def get_inventory(self, warehouse_id, goods_id):
        try:
            return Inventory.objects.get(warehouse_id=warehouse_id, goods_id=goods_id)
        except ObjectDoesNotExist:
            return None

    @transaction.atomic
    def add_inventory(self, warehouse_id, goods_id, quantity):
        try:
            inventory = Inventory.objects.select_for_update().get(
                warehouse_id=warehouse_id,
                goods_id=goods_id,

            )
            inventory.quantity += quantity
            inventory.save()
            return inventory
        except ObjectDoesNotExist:
            inventory = Inventory.objects.create(
                warehouse_id=warehouse_id,
                goods_id=goods_id,
                quantity=quantity
            )
            return inventory

    @transaction.atomic
    def deduct_inventory(self, warehouse_id, goods_id, quantity):
        try:
            inventory = Inventory.objects.select_for_update().get(
                warehouse_id=warehouse_id,
                goods_id=goods_id
            )
            if inventory.quantity < quantity:
                raise ValueError("Insufficient inventory")
            inventory.quantity -= quantity
            inventory.save()
            return inventory
        except ObjectDoesNotExist:
            raise ValueError("Inventory does not exist")

    def get_all_inventory(self):
        return Inventory.objects.select_related('warehouse', 'goods').all()

    def get_low_stock_items(self, threshold=10):
        return Inventory.objects.select_related('warehouse', 'goods').filter(quantity__lt=threshold)

    def get_inventory_by_id(self, inventory_id):
        try:
            return Inventory.objects.select_related('warehouse', 'goods').get(id=inventory_id)
        except ObjectDoesNotExist:
            return None

    def delete_inventory(self, inventory_id):
        try:
            inventory = Inventory.objects.get(id=inventory_id)
            inventory.delete()
        except ObjectDoesNotExist:
            pass