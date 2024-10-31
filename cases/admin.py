import logging

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import CaseAdminForm, CaseImageAdminForm, VehicleAdminForm
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
    form = VehicleAdminForm
    extra = 1
    verbose_name = _("Vehicle")
    verbose_name_plural = _("Vehicles")

    class Media:
        js = ("js/vehicle_admin.js",)


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    form = CaseImageAdminForm
    extra = 3
    verbose_name = _("Case Image")
    verbose_name_plural = _("Case Images")


@admin.register(AboutMessage)
class AboutMessageAdmin(admin.ModelAdmin):
    inlines = [AboutImageInline]
    list_display = ("title", "created_at", "updated_at")
    search_fields = ["title", "content"]

    class Meta:
        verbose_name = _("About Message")
        verbose_name_plural = _("About Messages")


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

    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    form = VehicleAdminForm
    change_form_template = "admin/cases/vehicle/vehicle_change_form.html"
    list_display = ("brand", "model", "year", "vehicle_type", "engine_capacity")
    list_filter = ("vehicle_type", "year")
    search_fields = ["brand", "model"]

    fieldsets = (
        (
            _("Basic Information"),
            {
                "fields": ("case", "vehicle_type", "brand", "model", "year"),
                "classes": ("wide",),
            },
        ),
        (
            _("Engine Details"),
            {
                "fields": ("engine_capacity",),
                "classes": ("wide",),  # Remove collapse to ensure visibility
            },
        ),
    )

    class Media:
        js = ("js/vehicle_admin.js",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.vehicle_type.name == VehicleType.ELECTRIC:
            form.fields["engine_capacity"].required = False
        return form

    def save_model(self, request, obj, form, change):
        if obj.vehicle_type.name == VehicleType.ELECTRIC:
            obj.engine_capacity = None
        super().save_model(request, obj, form, change)


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    form = CaseAdminForm
    inlines = [VehicleInline, CaseImageInline]
    list_display = ("title", "created_at", "main_page_visibility", "added_by")
    list_filter = ("main_page_visibility", "created_at")
    search_fields = ["title", "description"]
    readonly_fields = ("created_at", "updated_at")

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
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.added_by = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ("js/case_admin.js",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            _("Main Information"),
            {
                "fields": ("address", "phone_number", "email"),
            },
        ),
        (
            _("Social Media Links"),
            {
                "fields": ("instagram_link", "telegram_link"),
                "classes": ("collapse",),
            },
        ),
    )
    list_display = (
        "address",
        "phone_number",
        "email",
        "instagram_link",
        "telegram_link",
    )


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
