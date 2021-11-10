from rest_framework import serializers

from pstore.models import ItemCart, Product, Review


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
        fields = ('product_id', 'product_name', 'product_price', 'product_image', 'quantity')


class ItemCartsSerializer(serializers.Serializer):
    items = ItemCartSerializer(many=True)
