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
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    
class Case(models.Model):
    title = models.CharField(max_length=255)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = RichTextUploadingField()
    # Fields for images and videos (consider using ImageField, FileField)
    
class CaseImage(models.Model):
    """Images related to the case"""
    pass