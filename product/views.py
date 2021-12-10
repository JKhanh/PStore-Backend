from django.db.models import query
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, filters, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView

# Create your views here.
from product.models import Product
from product.serializer import ProductSerializer

# Create your views here.
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


class ProductDetailView(RetrieveAPIView):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return get_object_or_404(Product, id=kwargs.get('pk'))


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)