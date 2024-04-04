from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Case)
admin.site.register(VehicleType)
admin.site.register(Vehicle)
admin.site.register(FuelEngineVehicle)
admin.site.register(CaseImage)