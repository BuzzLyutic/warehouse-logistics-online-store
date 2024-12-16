from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsWarehouseStaff, IsAdmin
from .repositories import WarehouseRepository, GoodsRepository
from .serializers import InventorySerializer, WarehouseSerializer, GoodsSerializer
from .serializers import InventoryUpdateSerializer
from .repositories import InventoryRepository


class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can view
    lookup_field = 'id'


    def get_queryset(self):
        repository = InventoryRepository()
        return repository.get_all_inventory()


class InventoryDetailView(generics.RetrieveAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can view
    lookup_field = 'id'

    def get_queryset(self):
        repository = InventoryRepository()
        return repository.get_all_inventory()


class InventoryUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can update
    def post(self, request, format=None):
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            warehouse_id = serializer.validated_data['warehouse_id']
            goods_id = serializer.validated_data['goods_id']
            quantity = serializer.validated_data['quantity']
            action = serializer.validated_data.get('action', 'add')  # Default action

            inventory_repository = InventoryRepository()
            warehouse_repository = WarehouseRepository()
            goods_repository = GoodsRepository()

            warehouse = warehouse_repository.get_by_id(warehouse_id)
            goods = goods_repository.get_by_id(goods_id)

            if not warehouse or not goods:
                return Response({"error": "Warehouse or Goods not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                if action == 'add':
                    inventory = inventory_repository.add_inventory(warehouse_id, goods_id, quantity)
                elif action == 'deduct':
                    inventory = inventory_repository.deduct_inventory(warehouse_id, goods_id, quantity)
                else:
                    return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

                # Trigger observer (event publishing)
                from .tasks import publish_inventory_event
                publish_inventory_event.delay(inventory.id, action)

                return Response(InventorySerializer(inventory).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InventoryCreateView(APIView):
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can view
    def post(self, request, format=None):
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            warehouse_id = serializer.validated_data['warehouse_id']
            goods_id = serializer.validated_data['goods_id']
            quantity = serializer.validated_data['quantity']

            inventory_repository = InventoryRepository()
            warehouse_repository = WarehouseRepository()
            goods_repository = GoodsRepository()

            warehouse = warehouse_repository.get_by_id(warehouse_id)
            goods = goods_repository.get_by_id(goods_id)

            if not warehouse or not goods:
                return Response({"error": "Warehouse or Goods not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                inventory = inventory_repository.add_inventory(warehouse_id, goods_id, quantity)
                return Response(InventorySerializer(inventory).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InventoryDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  # Only admin can delete

    def delete(self, request, id, format=None):
        inventory_repository = InventoryRepository()
        inventory = inventory_repository.get_inventory_by_id(id)
        if not inventory:
            return Response({"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND)

        inventory_repository.delete_inventory(id)
        return Response({"message": "Inventory deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class WarehouseCreateView(generics.CreateAPIView):
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can view

    def post(self, request, *args, **kwargs):
        repository = WarehouseRepository()
        warehouse = repository.create(
            name=request.data.get('name'),
            location=request.data.get('location')
        )
        return Response(WarehouseSerializer(warehouse).data, status=status.HTTP_201_CREATED)


class WarehouseListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can view
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        repository = WarehouseRepository()
        return repository.get_all()

# Goods Views

class GoodsCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can view
    serializer_class = GoodsSerializer

    def post(self, request, *args, **kwargs):
        repository = GoodsRepository()
        goods = repository.create(
            sku=request.data.get('sku'),
            name=request.data.get('name'),
            description=request.data.get('description')
        )
        return Response(GoodsSerializer(goods).data, status=status.HTTP_201_CREATED)


class GoodsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsWarehouseStaff]  # Only staff or admin can view
    serializer_class = GoodsSerializer

    def get_queryset(self):
        repository = GoodsRepository()
        return repository.get_all()
