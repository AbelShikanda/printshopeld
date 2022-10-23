from decimal import Decimal
from django.conf import settings
from django.db import models

from shop.models import Product


class Order(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    county          = models.CharField(max_length=200, null=True, blank=True)
    town            = models.CharField(max_length=200, null=True, blank=True)
    estate          = models.CharField(max_length=200, null=True, blank=True)
    landmark        = models.CharField(max_length=200, null=True, blank=True)
    house_no        = models.CharField(max_length=200, null=True, blank=True)
    phone           = models.CharField(max_length=100)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    total_paid      = models.DecimalField(max_digits=10, decimal_places=2)
    order_key       = models.CharField(max_length=200)
    complete        = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
