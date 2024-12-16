from django.urls import path
from .views import InventoryListView, InventoryDetailView, InventoryUpdateView, InventoryDeleteView, \
    InventoryCreateView, WarehouseListView, WarehouseCreateView, GoodsListView, GoodsCreateView

urlpatterns = [
    path('inventory/', InventoryListView.as_view(), name='inventory-list'),
    path('inventory/<int:id>/', InventoryDetailView.as_view(), name='inventory-detail'),
    path('inventory/update/', InventoryUpdateView.as_view(), name='inventory-update'),
    path('inventory/create/', InventoryCreateView.as_view(), name='inventory-create'),
    path('inventory/delete/<int:id>/', InventoryDeleteView.as_view(), name='inventory-delete'),

    # Warehouse endpoints
    path('warehouse/', WarehouseListView.as_view(), name='warehouse-list'),
    path('warehouse/create/', WarehouseCreateView.as_view(), name='warehouse-create'),

    # Goods endpoints
    path('goods/', GoodsListView.as_view(), name='goods-list'),
    path('goods/create/', GoodsCreateView.as_view(), name='goods-create'),
]