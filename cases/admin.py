import logging

from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .models import (
    AboutImage,
    AboutMessage,
    Case,
    CaseImage,
    Contact,
    Service,
    ServiceCategory,
    Vehicle,
    VehicleType,
)

logger = logging.getLogger(__name__)


class AboutImageInline(admin.TabularInline):
    model = AboutImage
    extra = 1
    verbose_name = _("About Image")
    verbose_name_plural = _("About Images")


class VehicleInline(admin.StackedInline):
    model = Vehicle
    verbose_name = _("Vehicle")
    verbose_name_plural = _("Vehicles")


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 3
    verbose_name = _("Case Image")
    verbose_name_plural = _("Case Images")


@admin.register(AboutMessage)
class AboutMessageAdmin(admin.ModelAdmin):
    inlines = [AboutImageInline]
    list_display = ("title", "created_at", "updated_at")
    search_fields = ["title", "content"]

    # def get_app_label(self):
    #     return _("About Messages")

    class Meta:
        verbose_name = _("About Message")
        verbose_name_plural = _("About Messages")


# admin.site.register(AboutMessage, AboutMessageAdmin)


class ServiceInline(admin.StackedInline):
    model = Service
    extra = 1
    verbose_name = _("Service")
    verbose_name_plural = _("Services")


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "service_count", "created_at", "updated_at")
    inlines = [ServiceInline]
    search_fields = ["name"]

    def service_count(self, obj):
        return obj.services.count()

    service_count.short_description = _("Number of Services")

    # def get_app_label(self):
    #     return _("Service Categories")

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    change_form_template = "admin/cases/vehicle/vehicle_change_form.html"
    list_display = ("brand", "model", "year", "vehicle_type", "engine_capacity")
    list_filter = ("vehicle_type", "year")
    search_fields = ["brand", "model"]

    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ("case", "vehicle_type", "brand", "model", "year")},
        ),
        (
            _("Engine Details"),
            {
                "fields": ("engine_capacity",),
                "classes": ("collapse",),
            },
        ),
    )

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "update_engine_capacity/",
                self.update_engine_capacity,
                name="update_engine_capacity",
            ),
        ]
        return custom_urls + urls

    def update_engine_capacity(self, request):
        vehicle_type_id = request.GET.get("vehicle_type")
        try:
            vehicle_type = VehicleType.objects.get(id=vehicle_type_id)
            show_engine_capacity = vehicle_type.name in [
                VehicleType.FUEL_ENGINE,
                VehicleType.HYBRID,
            ]
        except VehicleType.DoesNotExist:
            show_engine_capacity = False

        context = {"show_engine_capacity": show_engine_capacity}
        html = render_to_string(
            "admin/cases/vehicle/engine_capacity_field.html", context
        )
        return HttpResponse(html)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    class Media:
        js = ("js/case_admin.js",)

    inlines = [VehicleInline, CaseImageInline]
    list_display = ("title", "created_at", "main_page_visibility", "added_by")
    list_filter = ("main_page_visibility", "created_at")
    search_fields = ["title", "description"]

    fieldsets = (
        (
            _("Basic Information"),
            {"fields": ("title", "description", "main_page_visibility", "added_by")},
        ),
        (
            _("Images"),
            {
                "fields": ("preview_image", "preview_image_alt"),
            },
        ),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "address",
        "phone_number",
        "email",
        "instagram_link",
        "telegram_link",
    )
    fieldsets = (
        (
            _("Main Information"),
            {
                "fields": (
                    "address",
                    "phone_number",
                    "email",
                ),
            },
        ),
        (
            _("Social Media Links"),
            {
                "fields": (
                    "instagram_link",
                    "telegram_link",
                ),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
