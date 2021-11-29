from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core import serializers

from rest_framework import status, generics, filters
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

# Create your views here.
from pstore.models import Cart, ItemCart, ItemOrder, Order, Product, Review
from pstore.serialize import OrderSerializer, ProductSerializer, ReviewSerializer, ItemCartsSerializer, ItemCartSerializer
from userprofile.models import UserProfile


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


class CartView(APIView):
    permisstion_classes = [IsAuthenticated]
    serializer_class = ItemCartSerializer

    def post(self, request, *args, **kwargs):
        serializers = ItemCartSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        obj, _ = Cart.objects.get_or_create(customer=request.user)
        product = get_object_or_404(Product, id=serializers.validated_data['product_id'])
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
            'id': item.id,
            'product_id': item.product.id,
            'product_name': item.product.name,
            'product_image': item.product.image,
            'product_price': item.product.basePrice,
            'date_created': int(item.date_created.timestamp()),
            'date_updated': int(item.date_updated.timestamp()),
            'quantity': item.quantity
        } for item in obj.items.all().order_by('-date_updated')]
        return JsonResponse({
            "items": items
        }, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        serializers = ItemCartSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        itemCart = get_object_or_404(ItemCart, id=serializers.validated_data['product_id'])
        itemCart.delete()
        return JsonResponse({
            'message': 'Delete item cart successful'
        }, status=status.HTTP_200_OK)
        

class OrderView(ListCreateAPIView):
    permisstion_classes = [IsAuthenticated]
    serializer_class = OrderSerializer


    def post(self, request, *args, **kwargs):
        items = ItemCartsSerializer(data=request.data.get('items'))
        items.is_valid(raise_exception=True)
        order = Order.objects.create(customer=request.user)
        order.save()
        for item in items.validated_data:
            orderItem, _ = ItemOrder.objects.update_or_create(
                order=order, product=item.get['product'], quantity=item.get['quantity'])
            orderItem.price = orderItem.product.basePrice*orderItem.quantity
            orderItem.save()
            order.items.add(orderItem)
        order.address = UserProfile.objects.get(user=request.user).address
        order.save()
        return JsonResponse({
            'order': OrderSerializer(data=order),
        }, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)


class PaymentAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(request.data.get('order_id'))
        if request.user == order.customer:
            order.paid = True
            order.save()

            for itemOrder in order.items.all():
                item = Cart.objects.get(customer=request.user).items.get(product=itemOrder.product)
                item.delete()

            return JsonResponse({
                'message': 'Payment successful'
            }, status=status.HTTP_201_CREATED)