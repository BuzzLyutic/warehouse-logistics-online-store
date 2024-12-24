from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Shipment, ShipmentLog
from .permissions import IsServiceAccount
from .serializers import ShipmentSerializer, ShipmentLogSerializer
from .tasks import notify_order_processing_service, simulate_shipment_updates
import datetime
from rest_framework import generics


class ShipmentListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer


class ShipmentCreateView(APIView):
    permission_classes = [IsServiceAccount]

    def post(self, request):
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            shipment = serializer.save()
            simulate_shipment_updates.delay(shipment.shipment_id) # Simulate after creation
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShipmentUpdateStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, shipment_id):
        shipment = Shipment.objects(shipment_id=shipment_id).first()
        if not shipment:
            return Response({'error': 'Shipment not found'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status', shipment.status)
        new_location = request.data.get('location')  # Get location from request

        # Only update if new status or location is provided
        if new_status != shipment.status or new_location:
            shipment.status = new_status
            shipment.updated_at = datetime.datetime.now()

            # Create and append a new log
            if new_location:  # Only create a log if location is provided
                log = ShipmentLog(
                    timestamp=datetime.datetime.now(),
                    location=new_location,
                    status=new_status
                )
                shipment.logs.append(log)

            shipment.save()
            # Notify other services if needed
            notify_order_processing_service.delay(shipment_id)

            return Response(ShipmentSerializer(shipment).data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No updates provided'}, status=status.HTTP_200_OK)

class ShipmentTrackingView(APIView):
    def get(self, request, shipment_id):
        shipment = Shipment.objects(shipment_id=shipment_id).first()
        if not shipment:
            return Response({'error': 'Shipment not found'}, status=status.HTTP_404_NOT_FOUND)

        logs = shipment.logs  # Access the logs field directly
        serializer = ShipmentLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
