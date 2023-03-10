from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os

from .models import Product, Carousel

@receiver(post_save, sender=Product)
@receiver(post_save, sender=Carousel)
def copy_image_to_static(sender, instance, **kwargs):
    image_path = os.path.join(settings.MEDIA_ROOT, instance.image.name)
    static_path = os.path.join(settings.STATIC_ROOT, 'images', instance.image.name)
    os.makedirs(os.path.dirname(static_path), exist_ok=True)
    with open(image_path, 'rb') as f:
        with open(static_path, 'wb') as f2:
            f2.write(f.read())

@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=Carousel)
def delete_image_from_static(sender, instance, **kwargs):
    static_path = os.path.join(settings.STATIC_ROOT, 'images', instance.image.name)
    os.remove(static_path)

