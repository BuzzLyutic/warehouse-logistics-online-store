from django.db import models


# Create your models here.
class Warehouse(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Goods(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    warehouse = models.ForeignKey(Warehouse, related_name='inventories', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, related_name='inventories', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'goods')

    def __str__(self):
        return f"{self.goods} in {self.warehouse}: {self.quantity}"


class ProcessedOrderItem(models.Model):
    order_item_id = models.IntegerField(unique=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order Item ID: {self.order_item_id} processed at {self.processed_at}"
