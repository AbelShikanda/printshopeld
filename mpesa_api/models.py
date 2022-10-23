from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaPayment(BaseModel):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    description = models.TextField()
    phone_number = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.TextField()
    
    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
        
    def __str__(self):
        return self.first_name

class LipaNaMpesaOnline(models.Model):
    checkout_request_ID = models.CharField(max_length=255, blank=True, null=True)
    merchant_request_ID = models.CharField(max_length=255, blank=True, null=True)
    result_desc = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=255, blank=True, null=True)
    transaction_date = models.DateTimeField()
    phone_number = models.IntegerField()
    
    def __str__(self):
        return self.receipt_number
    
    class Meta:
        verbose_name_plural = 'Lipa Na Mpesa Online'