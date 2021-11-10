from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers

from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# Create your views here.
from pstore.models import Cart, ItemCart, Product, Review
from pstore.serialize import ProductSerializer, ReviewSerializer, ItemCartsSerializer


class ListCreateProductView(ListCreateAPIView):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return Product.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': 'Created new Product successful'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create Product failed'
        }, status=status.HTTP_400_BAD_REQUEST)


class ListReviewByProduct(ListCreateAPIView):
    model = Review
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs.get('pk'))
        return Review.objects.filter(product=product)


class ProductSearchView(generics.ListCreateAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class CartView(ListCreateAPIView):
    permisstion_classes = [IsAuthenticated]
    serializer_class = ItemCartsSerializer

    def post(self, request, *args, **kwargs):
        obj, _ = Cart.objects.get_or_create(customer=request.user)
        product = get_object_or_404(Product, id=request.data.get('product_id'))
        # product.is_valid(raise_exception=True)
        item, itemCreated = ItemCart.objects.update_or_create(
            cart=obj, product=product
        )
        if itemCreated == False:
            item.quantity += 1
        obj.items.add(item)
        item.save()
        obj.save()
        return JsonResponse({
            'message': 'Added to cart successful'
        }, status=status.HTTP_201_CREATED)
    
    def get(self, request, *args, **kwargs):
        obj, _ = Cart.objects.get_or_create(customer=request.user)
        items = [{
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_image': item.product.image,
            'product_price': item.product.basePrice,
            'quantity': item.quantity
        } for item in obj.items.all()]
        return JsonResponse({
            "items": items
        }, status=status.HTTP_200_OK)
        

    