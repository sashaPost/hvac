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
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    
class FuelEngineVehicle(Vehicle):
    engine_capacity = models.DecimalField(max_digits=3, decimal_places=1)
    
class Case(models.Model):
    title = models.CharField(max_length=255)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    description = RichTextUploadingField()
    preview_image = models.ImageField(upload_to='images')
    preview_image_alt = models.CharField(max_length=255, blank=True)
    
    # !!! haven't migrated yet
    # main_page_visibility = models.BooleanField(default=True)
    
class CaseImage(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    image_alt = models.CharField(max_length=255, blank=True)