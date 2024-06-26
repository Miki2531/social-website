from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image

@receiver(m2m_changed, sender=Image.user_likes.through)
def user_like_changes(sender, instance, **kwargs):
    instance.total_likes = instance.user_likes.count()
    instance.save()