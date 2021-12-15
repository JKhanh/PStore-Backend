from django.db.models import query
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, generics, filters, viewsets
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

# Create your views here.
from product.models import Product
from product.recommend import Recommend
from product.serializer import ProductSerializer

# Create your views here.
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 60 * 24))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductRecommendView(RetrieveAPIView):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    recommended = Recommend()

    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['pk'])
        recommended_products = self.recommended.recommend_by_item(product.image)
        products = []
        for id, asin in recommended_products:
            product_rec = get_object_or_404(Product, asin)
            products.append(product_rec)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        