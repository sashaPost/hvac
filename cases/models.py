import logging

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field
from phonenumber_field.modelfields import PhoneNumberField

logger = logging.getLogger(__name__)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(_("Created At"), default=timezone.now)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True


class AboutMessage(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    content = CKEditor5Field(_("Text"), config_name="extends")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("About Message")
        verbose_name_plural = _("About Messages")
        # verbose_name = "Повідомлення про нас"  # Hardcode the Ukrainian translation
        # verbose_name_plural = "Повідомлення про нас"  # Hardcode the Ukrainian translation


class AboutImage(models.Model):
    about_image = models.ForeignKey(
        AboutMessage,
        verbose_name=_("About Message"),
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(_("Image"), upload_to="images")
    image_alt = models.CharField(_("Image Alt"), max_length=255, blank=True)

    def __str__(self):
        return self.image_alt or str(_("Image"))

    class Meta:
        verbose_name = _("About Image")
        verbose_name_plural = _("About Images")


class ServiceCategory(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")
        # verbose_name = "Категорія послуг"  # Hardcode the Ukrainian translation
        # verbose_name_plural = "Категорії послуг"  # Hardcode the Ukrainian translation
        ordering = ["name"]


class Service(TimeStampedModel):
    category = models.ForeignKey(
        ServiceCategory,
        verbose_name=_("Category"),
        on_delete=models.CASCADE,
        related_name="services",
    )
    title = models.CharField(_("Title"), max_length=255)
    description = CKEditor5Field(_("Description"), config_name="extends")
    icon = models.ImageField(_("Icon"), upload_to="images", blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return f"{self.category.name} - {self.title}"

    class Meta:
        ordering = ["category", "title"]
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        indexes = [models.Index(fields=["is_active"])]


class Case(TimeStampedModel):
    title = models.CharField(_("Title"), max_length=255)
    description = CKEditor5Field(_("Text"), config_name="extends")
    preview_image = models.ImageField(_("Preview Image"), upload_to="images")
    preview_image_alt = models.CharField(
        _("Preview Image Alt"), max_length=255, blank=True
    )
    main_page_visibility = models.BooleanField(_("Main Page Visibility"), default=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Added By"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{_('Case')} #{self.id}: {self.title}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Case")
        verbose_name_plural = _("Cases")
        indexes = [
            models.Index(fields=["main_page_visibility"]),
        ]


class VehicleType(models.Model):
    FUEL_ENGINE = "FE"
    ELECTRIC = "EV"
    HYBRID = "HY"
    CAR_TYPE_CHOICES = [
        (FUEL_ENGINE, _("Fuel Engine")),
        (ELECTRIC, _("Electric Vehicle")),
        (HYBRID, _("Hybrid Vehicle")),
    ]
    name = models.CharField(
        _("Type"), max_length=100, choices=CAR_TYPE_CHOICES, db_index=True
    )

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = _("Vehicle Type")
        verbose_name_plural = _("Vehicle Types")


class Vehicle(models.Model):
    case = models.OneToOneField(
        Case, verbose_name=_("Case"), on_delete=models.CASCADE, related_name="vehicle"
    )
    vehicle_type = models.ForeignKey(
        VehicleType,
        verbose_name=_("Vehicle Type"),
        on_delete=models.CASCADE,
        related_name="vehicles",
    )
    brand = models.CharField(_("Brand"), max_length=100)
    model = models.CharField(_("Model"), max_length=100)
    year = models.PositiveIntegerField(
        _("Year"),
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(timezone.now().year + 1),
        ],
    )
    engine_capacity = models.DecimalField(
        _("Engine Capacity"),
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        help_text=_("In litres"),
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
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")


class CaseImage(TimeStampedModel):
    case = models.ForeignKey(
        Case,
        related_name="case",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(_("Image"), upload_to="images")
    image_alt = models.CharField(_("Image Alt"), max_length=255, blank=True)

    def __str__(self):
        return f"{_('Image for')} {self.case}"

    class Meta:
        verbose_name = _("Case Image")
        verbose_name_plural = _("Case Images")


class Contact(TimeStampedModel):
    address = models.CharField(_("Address"), max_length=255)
    phone_number = PhoneNumberField(_("Phone Number"))
    email = models.EmailField(_("Email"))
    instagram_link = models.URLField(_("Instagram"), blank=True)
    telegram_link = models.URLField(_("Telegram"), blank=True)

    def __str__(self):
        return str(_("Contact Information"))

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
