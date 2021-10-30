import datetime

from django.db import models


# Create your models here.
from django.utils import timezone


class Product(models.Model):
    ProductType = (
        ('PH', 'Phone'),
        ('AC', 'Accessory'),
        ('EL', 'Electronic'))

    name = models.CharField(max_length=500)
    type = models.CharField(choices=ProductType, default='PH', max_length=2)
    basePrice = models.FloatField(default=0)
    sale = models.FloatField(default=0)
    image = models.CharField(max_length=1000)


class Customer(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=100)
    birthday = models.DateField()
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('U', 'Unisex'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    phone_number = models.CharField(max_length=17, blank=True)


class Review(models.Model):
    reviewer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.CharField(max_length=500)
    dateCreated = models.DateField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    is_in_order = models.BooleanField(default=False)


class ItemCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class ItemOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

