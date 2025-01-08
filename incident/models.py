from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from customauth.models import CustomUserModel


import uuid

# Create your models here.


# Create your models here.

class Incident(models.Model):
    incident_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    user_input_location = models.CharField(max_length=100)
    live_location = models.PointField(geography=True,null=True,blank=True)
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
            ('other', 'Other'),
        ],
        default='other'
    )
    date_reported = models.DateTimeField(auto_now_add=True)  # When the incident was reported
    incident_date = models.DateTimeField()  # When the incident occurred
    resolved = models.BooleanField(default=False) 
    status = models.CharField(
        max_length=20,
        choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('closed', 'Closed')],
        default='open'
    )
