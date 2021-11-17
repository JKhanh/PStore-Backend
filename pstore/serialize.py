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


class ItemCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCart
        fields = ('product', 'quantity')
        depth = 1

    def create(self, validated_data):
        return ItemCart.objects.create(product=Product.objects.get(id=validated_data.get('product_id')))

class ItemCartsSerializer(serializers.Serializer):
    items = ItemCartSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = '__all__'