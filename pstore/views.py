from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
from pstore.models import Cart, ItemCart, Product, Review
from pstore.serialize import ProductSerializer, ReviewSerializer


class ListCreateProductView(ListCreateAPIView):
    model = Product
    serializer_class = ProductSerializer

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


class CartView(generics.ListCreateAPIView):
    model = Product
    serializer_class = ProductSerializer
    permisstion_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        obj, _ = Cart.objects.get_or_create(user=request.user)
        product = ProductSerializer(data=request.data)
        if product.is_valid():
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

        else:
            return JsonResponse({
                'message': 'Add to cart failed'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        obj, _ = Cart.objects.get_or_create(user=request.user)
        return obj.items.all()

    