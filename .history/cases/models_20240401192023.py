from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class VehicleType(models.Model):
    FUEL_ENGINE = 'FE'
    ELECTRIC = 'EV'
    CAR_TYPE_CHOICES = [
        (FUEL_ENGINE, 'Fuel Engine'), 
        (ELECTRIC, 'Electric Vehicle'),        
    ]
    name = models.CharField(max_length=100, choices=CAR_TYPE_CHOICES)
    
class Vehicle(models.Model):
    car_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)