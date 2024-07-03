from django.contrib import admin
from .models import (
    AboutImage,
    AboutMessage,
    Case,
    VehicleType,
    Vehicle,
    CaseImage,
)
import logging


logger = logging.getLogger(__name__)


class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1


class AboutMessageAdmin(admin.ModelAdmin):
    inlines = [AboutImageInline]


admin.site.register(AboutMessage, AboutMessageAdmin)


@admin.register(VehicleType)
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    js = ("js/vehicle_admin.js",)


class VehicleInline(admin.StackedInline):
    model = Vehicle


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 3


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/case_admin.js",)

    inlines = [VehicleInline, CaseImageInline]
