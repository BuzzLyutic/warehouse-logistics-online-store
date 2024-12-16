import mongoengine as me
import datetime


class ShipmentLog(me.EmbeddedDocument):
    timestamp = me.DateTimeField(default=datetime.datetime.now)
    location = me.StringField(max_length=255)
    status = me.StringField(max_length=50)

    def __str__(self):
        return f"{self.status} @ {self.location}"


class Shipment(me.Document):
    shipment_id = me.StringField(max_length=255, unique=True, required=True)
    order_id = me.StringField(max_length=255, required=True)
    carrier_name = me.StringField(max_length=255, required=True)
    tracking_number = me.StringField(max_length=255, null=True, blank=True)
    status = me.StringField(max_length=50, default='created')
    estimated_delivery = me.DateTimeField(null=True, blank=True)
    created_at = me.DateTimeField(default=datetime.datetime.now, required=False)
    updated_at = me.DateTimeField(default=datetime.datetime.now, required=False)
    logs = me.EmbeddedDocumentListField(ShipmentLog, default=list)  # Added logs field

    meta = {'collection': 'shipments'} # Ensure correct collection name in MongoDB

    def __str__(self):
        return self.shipment_id

