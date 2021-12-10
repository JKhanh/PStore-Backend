from product.views import ProductViewSet
from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

product_list = ProductViewSet.as_view({
    'get': 'list',
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
})

urlpatterns = format_suffix_patterns([
    path(r'products/', product_list, name='product-list'),
    path(r'products/<int:pk>/', product_detail, name="product-detail"),
])
    