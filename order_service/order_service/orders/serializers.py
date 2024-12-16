from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['goods_id', 'quantity', 'warehouse_id']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'status']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', [])
        instance = super().update(instance, validated_data)

        if order_items_data:
            instance.order_items.all().delete()  # Clear existing items
            for item_data in order_items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance
