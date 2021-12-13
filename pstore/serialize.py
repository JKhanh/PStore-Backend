from rest_framework import serializers

from pstore.models import Order


class ItemCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()

class ItemCartsSerializer(serializers.Serializer):
    items = ItemCartSerializer(many=True, partial=True)


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'