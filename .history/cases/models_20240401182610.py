from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class CarType(models.Model):
    FUEL_ENGINE = 'FE'
    ELECTRIC = 'EV'
    CAR_TYPE_CHOICES = [
        (FUEL_ENGINE, 'Fuel Engine'), 
        (ELECTRIC, 'Electric Vehicle'),        
    ]