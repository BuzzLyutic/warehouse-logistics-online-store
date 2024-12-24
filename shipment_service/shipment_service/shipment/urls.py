from django.urls import path
from .views import ShipmentCreateView, ShipmentUpdateStatusView, ShipmentTrackingView, ShipmentListView

urlpatterns = [
    path('shipments/', ShipmentCreateView.as_view(), name='create_shipment'),
    path('shipments/<str:shipment_id>/', ShipmentUpdateStatusView.as_view(), name='update_shipment_status'),
    path('shipments/<str:shipment_id>/tracking/', ShipmentTrackingView.as_view(), name='track_shipment'),
    path('all_shipments/', ShipmentListView.as_view(), name='all_shipments'),

]
