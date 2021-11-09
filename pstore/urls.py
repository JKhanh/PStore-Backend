from django.urls import path

from pstore.views import ListCreateProductView, ListReviewByProduct, CartView

urlpatterns = [
    path(r'^products', ListCreateProductView.as_view()),
    path(r'^products/<int:pk>/reviews$', ListReviewByProduct.as_view()),
    path(r'^cart', CartView.as_view()),
]