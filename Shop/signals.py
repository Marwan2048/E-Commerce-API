from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Cart


@receiver(post_save , sender = User)
def create_cart(instance ,created , *args ,**kwargs):
    if created:
        Cart.objects.create(user = instance)