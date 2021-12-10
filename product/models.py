from django.db import models
from django.utils import timezone

from authenticate.models import User

# Create your models here.
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

    class Meta:
        db_table = 'pstore_product'


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.CharField(max_length=500)
    dateCreated = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'pstore_review'