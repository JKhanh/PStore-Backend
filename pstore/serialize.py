from rest_framework import serializers

from pstore.models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'type', 'basePrice', 'sale', 'image')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('reviewer', 'product', 'rate', 'comment')
