from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def fix_rate(sender, instance,  **kwargs):
    if instance.price > 5: 
        instance.price = 11 
        # demonstrating > if instance price is greater than 5 , then it sets the product
        #price to 11 , if its less than or equals to 5, product price will be set normally