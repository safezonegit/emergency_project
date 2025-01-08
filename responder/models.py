from django.db import models
from customauth.models import CustomUserModel

# Create your models here.

class SecurityResponder(models.Model):
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phonecall_contact = models.CharField(max_length=11)
    sms_contact = models.CharField(max_length=11,null=True,blank=True)
    emergency_contact = models.CharField(max_length=11,null=True,blank=True)


    def  __str__(self):
        return f"{self.name}"




class FireHazardResponder(models.Model):
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phonecall_contact = models.CharField(max_length=11)
    sms_contact = models.CharField(max_length=11,null=True,blank=True)
    emergency_contact = models.CharField(max_length=11,null=True,blank=True)

    def  __str__(self):
        return f"{self.name}"




class MedicalResponder(models.Model):
    user = models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phonecall_contact = models.CharField(max_length=11)
    sms_contact = models.CharField(max_length=11,null=True,blank=True)
    emergency_contact = models.CharField(max_length=11,null=True,blank=True)


    def  __str__(self):
        return f"{self.name}"