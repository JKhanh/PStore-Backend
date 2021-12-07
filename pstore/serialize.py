from rest_framework import serializers

from pstore.models import ItemCart, Order, Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('reviewer', 'product', 'rate', 'comment')


class ItemCartSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()

class ItemCartsSerializer(serializers.Serializer):
    items = ItemCartSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'