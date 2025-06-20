from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Tool

@receiver(pre_save, sender=Tool)
def generate_tool_id(sender, instance, **kwargs):
    if not instance.id:
        last_tool = Tool.objects.order_by('-id').first()
        if last_tool and last_tool.id.startswith('tool-'):
            next_id = int(last_tool.id.split('-')[1]) + 1
        else:
            next_id = 1
        instance.id = f"tool-{next_id}"