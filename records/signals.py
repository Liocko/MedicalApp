from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import MedicalRecord


@receiver(post_save, sender=MedicalRecord)
def notify_new_record(sender, instance, created, **kwargs):
    if not created:
        return
    channel_layer = get_channel_layer()
    if channel_layer is None:
        return
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "notification.message",
            "message": {
                "type": "new_record",
                "patient": str(instance.patient),
                "title": instance.title,
                "doctor": str(instance.doctor),
            },
        },
    )
