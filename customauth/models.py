from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class CustomUserModel(AbstractUser):
    username = models.CharField(max_length=255,null=True,blank=True)
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4(), unique=True)
    email = models.EmailField(unique=True)
    
    phone_number = models.CharField(max_length=15,null=False,blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email