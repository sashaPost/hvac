import logging

from django.conf import settings  # To access the User model
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone  # For default timestamps
from django_ckeditor_5.fields import CKEditor5Field
from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger(__name__)


class AboutMessage(models.Model):
    title = models.CharField(max_length=255)
    content = CKEditor5Field("Text", config_name="extends")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "About Message"
        verbose_name_plural = "About Messages"


class AboutImage(models.Model):
    about_image = models.ForeignKey(
        AboutMessage, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="images")
    image_alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.image_alt or "Image"

    class Meta:
        verbose_name = "About Image"
        verbose_name_plural = "About Images"


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"


class Service(models.Model):
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.CASCADE, related_name="services"
    )
    title = models.CharField(max_length=255)
    description = CKEditor5Field("Description", config_name="extends")
    icon = models.ImageField(upload_to="images", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["category", "title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"


class Case(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    description = CKEditor5Field("Text", config_name="extends")
    preview_image = models.ImageField(upload_to="images")
    preview_image_alt = models.CharField(max_length=255, blank=True)
    main_page_visibility = models.BooleanField(default=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Case #{self.id}: {self.title}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Case"
        verbose_name_plural = "Cases"


class VehicleType(models.Model):
    FUEL_ENGINE = "FE"
    ELECTRIC = "EV"
    HYBRID = "HY"
    CAR_TYPE_CHOICES = [
        (FUEL_ENGINE, "Fuel Engine"),
        (ELECTRIC, "Electric Vehicle"),
        (HYBRID, "Hybrid Vehicle"),
    ]
    name = models.CharField(max_length=100, choices=CAR_TYPE_CHOICES)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"


class Vehicle(models.Model):
    case = models.OneToOneField(Case, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    engine_capacity = models.DecimalField(
        max_digits=3, decimal_places=1, blank=True, null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_vehicle_type = self.vehicle_type_id if self.pk else None

    def save(self, *args, **kwargs):
        if self.pk:
            if self.vehicle_type_id != self._original_vehicle_type:
                if self.vehicle_type.name == VehicleType.ELECTRIC:
                    self.engine_capacity = None
        super().save(*args, **kwargs)
        self._original_vehicle_type = self.vehicle_type_id

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"


class CaseImage(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")
    image_alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.case}"

    class Meta:
        verbose_name = "Case Image"
        verbose_name_plural = "Case Images"


class Contact(models.Model):
    address = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    instagram_link = models.URLField(blank=True)
    telegram_link = models.URLField(blank=True)

    def __str__(self):
        return f"Contact Information"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
