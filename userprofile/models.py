from django.db import models
import uuid

from authenticate.models import User

# Create your models here.
class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True, unique=False)
    last_name = models.CharField(max_length=50, blank=True, unique=False)
    phone_number = models.CharField(max_length=12, blank=False, unique=True, null=False)
    address = models.CharField(max_length=100, blank=True, unique=False)
    birth_date = models.DateField(null=True, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unique'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        db_table = 'profile'