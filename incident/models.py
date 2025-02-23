from django.db import models
from customauth.models import CustomUserModel


import uuid

# Create your models here.


# Create your models here.

class Incident(models.Model):
    incident_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    user_input_location = models.CharField(max_length=100)
    live_location = models.CharField(max_length= 200, null=True,blank=True)
    severity = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')],
        default='low'
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('medical', 'Medical'),
            ('fire', 'Fire'),
            ('security', 'Security'),
        ],
        default='medical'
    )
    date_reported = models.DateTimeField(auto_now_add=True)  # When the incident was reported
    incident_date = models.DateTimeField(null=True,blank=True)  # When the incident occurred
    resolved = models.BooleanField(default=False) 
    status = models.CharField(
        max_length=20,
        choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')],
        default='open'
    )

    def __str__(self):
        return f"{self.user.first_name}{self.user.last_name}||{self.category}||{self.severity}"
