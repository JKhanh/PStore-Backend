from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

import product.recommend as recommend
# Create your views here.
from product.models import Product
from product.serializer import ProductSerializer

# Create your views here.
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('-basePrice')
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60 * 60 * 24))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductRecommendView(RetrieveAPIView):
    model = Product
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)

    @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['pk'])
        recommended_products = recommend.recommend(product.image)
        products = []
        for p in recommended_products:
            asin = p['asin']
            if asin == product.id: continue
            product_rec = Product.objects.filter(id=asin).first()
            if product_rec is None: continue
            products.append(product_rec)
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        