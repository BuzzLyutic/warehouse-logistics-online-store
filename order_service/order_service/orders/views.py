from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .tasks import process_order_task, fulfill_order_task, cancel_order_task, update_order_status_from_shipment, \
    publish_order_processing_event


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Trigger order processing after order is created
        order_id = serializer.data['id']
        process_order_task.delay(order_id)
        # publish_order_processing_event.delay(order_id, "created")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        order = self.get_object()
        process_order_task.delay(order.id)
        return Response({'status': 'processing started'})

    @action(detail=True, methods=['post'])
    def fulfill(self, request, pk=None):
        order = self.get_object()
        fulfill_order_task.delay(order.id)
        return Response({'status': 'fulfillment started'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        cancel_order_task.delay(order.id)
        return Response({'status': 'cancellation started'})

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """Endpoint to receive shipment status updates."""
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status:
            update_order_status_from_shipment.delay(order.id, new_status)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({'error': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)
