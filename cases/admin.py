import logging

from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string

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


class VehicleInline(admin.StackedInline):
    model = Vehicle


class CaseImageInline(admin.TabularInline):
    model = CaseImage
    extra = 3


class AboutMessageAdmin(admin.ModelAdmin):
    inlines = [AboutImageInline]


admin.site.register(AboutMessage, AboutMessageAdmin)


class ServiceInline(admin.StackedInline):
    model = Service
    extra = 1


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "service_count",
    )
    inlines = [ServiceInline]

    def service_count(self, obj):
        return obj.services.count()

    service_count.short_description = "Number of Services"


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    change_form_template = "admin/cases/vehicle/vehicle_change_form.html"

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
            "Main Block",
            {
                "fields": (
                    "address",
                    "phone_number",
                    "email",
                ),
            },
        ),
        (
            "Social Media Links",
            {
                "fields": (
                    "instagram_link",
                    "telegram_link",
                ),
                "classes": ("collapse",),
            },
        ),
    )


# @admin.register(ServiceCategory)
# class ServiceCategoryAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "service_count",
#     )
#
#     def service_count(self, obj):
#         return obj.services.count()
#     service_count.short_description = "Number of Services"
#
#
# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = (
#         "category",
#         "title",
#         "is_active",
#         "created_at",
#         "updated_at",
#     )
#     list_filter = ("category", "is_active")
#     search_fields = ("title", "description")
#     readonly_fields = ("created_at", "updated_at")
#     fieldsets = (
#         (None, {
#             'fields': ('category', 'title', 'description', 'icon', 'is_active')
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',),
#         }),
#     )
#     actions = ["make_active", "make_inactive"]
#     # inlines = [ServiceInline]
#
#     def make_active(self, request, queryset):
#         queryset.update(is_active=True)
#     make_active.short_description = "Mark selected services as active"
#
#     def make_inactive(self, request, queryset):
#         queryset.update(is_active=False)
#     make_inactive.short_description = "Mark selected services as inactive"
#
