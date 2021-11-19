import datetime

from django.db import models
from authenticate.models import User

# Create your models here.
from django.utils import timezone


class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=500)
    basePrice = models.FloatField(default=0)
    brand = models.CharField(max_length=500)
    category = models.CharField(max_length=500)
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=1000)
    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.CharField(max_length=500)
    dateCreated = models.DateField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


class Cart(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    is_in_order = models.BooleanField(default=False)


class ItemCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

