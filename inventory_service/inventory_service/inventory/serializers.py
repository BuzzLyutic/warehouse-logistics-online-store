from rest_framework import serializers
from .models import Warehouse, Goods, Inventory


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']


class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goods
        fields = ['id', 'sku', 'name', 'description']


class InventorySerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    goods = GoodsSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'warehouse', 'goods', 'quantity']


class InventoryUpdateSerializer(serializers.Serializer):
    warehouse_id = serializers.IntegerField()
    goods_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    action = serializers.CharField(required=False)

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
