from django import forms
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    AboutMessage,
    Case,
    CaseImage,
    Contact,
    Service,
    Vehicle,
    VehicleType,
)


class AdminBaseModelForm(forms.ModelForm):
    """
    Base form class for admin forms with common validation functionality.
    """

    def clean(self):
        cleaned_data = super().clean()
        for field_name, field in self.fields.items():
            if field.required and not cleaned_data.get(field_name):
                self.add_error(field_name, _("This field is required."))
        return cleaned_data


class VehicleAdminForm(AdminBaseModelForm):
    """
    Enhanced form for Vehicle model in admin interface with dynamic validation
    based on vehicle type.
    """

    class Meta:
        model = Vehicle
        fields = ["vehicle_type", "brand", "model", "year", "engine_capacity"]
        widgets = {
            "year": forms.NumberInput(
                attrs={
                    "min": 1900,
                    "class": "vYearField",
                }
            ),
            "engine_capacity": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0.1",
                    "max": "9.9",
                    "class": "vEngineCapacityField",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["engine_capacity"].required = False

        # Add custom CSS classes for admin styling
        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "vTextField"})

    def clean(self):
        cleaned_data = super().clean()
        vehicle_type = cleaned_data.get("vehicle_type")
        engine_capacity = cleaned_data.get("engine_capacity")

        if vehicle_type and engine_capacity:
            if vehicle_type.name == VehicleType.ELECTRIC:
                cleaned_data["engine_capacity"] = None
            elif (
                vehicle_type.name in [VehicleType.FUEL_ENGINE, VehicleType.HYBRID]
                and not engine_capacity
            ):
                self.add_error(
                    "engine_capacity",
                    _("Engine capacity is required for this vehicle type."),
                )

        return cleaned_data


class CaseAdminForm(AdminBaseModelForm):
    """
    Enhanced form for Case model in admin interface with image validation
    and custom widget for description.
    """

    class Meta:
        model = Case
        fields = [
            "title",
            "description",
            "preview_image",
            "preview_image_alt",
            "main_page_visibility",
            "added_by",
        ]
        widgets = {
            "description": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name="extends",
            ),
        }

    def clean_preview_image(self):
        image = self.cleaned_data.get("preview_image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                _("Image file too large. Size should not exceed 5MB.")
            )
        return image


class CaseImageAdminForm(AdminBaseModelForm):
    """
    Enhanced form for CaseImage model in admin interface with image validation
    """

    class Meta:
        model = CaseImage
        fields = ["image", "image_alt"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                _("Image file too large. Size should not exceed 5MB.")
            )
        return image


class LanguageSwitchForm(forms.Form):
    """
    Form for handling language switching in the frontend.
    """

    language = forms.ChoiceField(
        choices=[("uk", "UA"), ("en", "EN")],
        widget=forms.Select(
            attrs={
                "class": "form-select form-select-sm",
                "hx-post": "/set-language/",
                "hx-trigger": "change",
                "hx-swap": "none",
            }
        ),
    )
    next = forms.CharField(widget=forms.HiddenInput())
