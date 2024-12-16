from django.db import models
from django_fsm import FSMField, transition


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipping', 'Shipped'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # FSM status field
    status = FSMField(default='pending', choices=STATUS_CHOICES)

    @transition(field=status, source='pending', target='processing')
    def process_order(self):
        # Add task to pick, pack, and reserve inventory
        print("Order is now in processing state")

    @transition(field=status, source='processing', target='shipping')
    def ship_order(self):
        # Transition to the 'shipped' state
        print("Order is now in shipping state")

    @transition(field=status, source='shipping', target='fulfilled')
    def fulfill_order(self):
        # Fulfill the order (e.g., notify shipment service)
        print("Order is now fulfilled")

    @transition(field=status, source=['pending', 'processing'], target='cancelled')
    def cancel_order(self):
        # Reverse inventory and cancel the order
        print("Order is now cancelled")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    goods_id = models.IntegerField()
    quantity = models.IntegerField()
    warehouse_id = models.IntegerField()

    def __str__(self):
        return f"OrderItem for Order {self.order.id}, Goods ID: {self.goods_id}, Quantity: {self.quantity}, Warehouse ID: {self.warehouse_id}"
