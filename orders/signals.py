from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver
from orders.models import Order
from orders.services import send_order_confirmation_email

@receiver(post_save, sender=Order)
def send_email_on_order(sender, instance, created, **kwargs):
    if created: 
        transaction.on_commit(lambda: send_order_confirmation_email(instance.user, instance))
