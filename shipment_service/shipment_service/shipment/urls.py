from django.urls import path
from .views import ShipmentCreateView, ShipmentUpdateStatusView, ShipmentTrackingView

urlpatterns = [
    path('shipments/', ShipmentCreateView.as_view(), name='create_shipment'),
    path('shipments/<str:shipment_id>/', ShipmentUpdateStatusView.as_view(), name='update_shipment_status'),
    path('shipments/<str:shipment_id>/tracking/', ShipmentTrackingView.as_view(), name='track_shipment'),
]
