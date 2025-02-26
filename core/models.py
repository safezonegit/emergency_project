from django.db import models

# Create your models here.
class AnonymousResponse(models.Model):
   phone_number = models.CharField(max_length=12)
   message = models.TextField()

   def __str__(self):
      return f"{self.phone_number}||{self.message}"