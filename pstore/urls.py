from django.urls import path
from django.conf.urls import url

from pstore.views import ListCreateProductView, ListReviewByProduct, CartView

urlpatterns = [
    url(r'^products', ListCreateProductView.as_view()),
    url(r'^products/<int:pk>/reviews$', ListReviewByProduct.as_view()),
    url(r'^cart', CartView.as_view()),
]