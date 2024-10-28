from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Vehicle, VehicleType


@receiver(pre_save, sender=Vehicle)
def update_engine_capacity(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Vehicle.objects.get(pk=instance.pk)
            if (
                old_instance.vehicle_type != instance.vehicle_type
                and instance.vehicle_type.name == VehicleType.ELECTRIC
            ):
                instance.engine_capacity = None
        except Vehicle.DoesNotExist:
            pass
