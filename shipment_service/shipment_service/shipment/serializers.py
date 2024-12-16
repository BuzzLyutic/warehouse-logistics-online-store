from rest_framework import serializers
from .models import Shipment, ShipmentLog
import datetime


class ShipmentSerializer(serializers.Serializer):
    shipment_id = serializers.CharField(max_length=255)
    order_id = serializers.CharField(max_length=255)
    carrier_name = serializers.CharField(max_length=255)
    tracking_number = serializers.CharField(max_length=255, allow_blank=True, required=False)
    status = serializers.CharField(max_length=50, default='created')
    estimated_delivery = serializers.DateTimeField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(default=datetime.datetime.now)
    updated_at = serializers.DateTimeField(default=datetime.datetime.now)
    logs = serializers.SerializerMethodField()

    def get_logs(self, obj):
        return ShipmentLogSerializer(obj.logs, many=True).data

    def create(self, validated_data):
        shipment = Shipment.objects.create(**validated_data)
        return shipment

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.updated_at = datetime.datetime.now()
        instance.save()
        return instance


class ShipmentLogSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    location = serializers.CharField(max_length=255)
    status = serializers.CharField(max_length=50)

    def create(self, validated_data):
        return ShipmentLog(**validated_data)


'''

        
        
class ShipmentLogSerializer(mongo_serializers.EmbeddedDocumentSerializer): # Use mongoengine serializer
    class Meta:
        model = ShipmentLog
        fields = '__all__'


class ShipmentSerializer(serializers.DocumentSerializer):
    logs = ShipmentLogSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'
'''
