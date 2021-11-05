from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

# Create your views here.
from pstore.models import Product, Review
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
