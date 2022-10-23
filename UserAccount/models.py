from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
# Create your models here.

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    
    # email           = models.EmailField(unique=True, verbose_name="Email Address")
    email           = models.EmailField(_('email address'), unique=True)
    user_name       = models.CharField(max_length=200)
    first_name      = models.CharField(max_length=100)
    last_name       = models.CharField(max_length=100, blank=True)
    TYPE_SELECT     = (('0', 'Female'),('1', 'male'),)
    gender          = models.CharField(max_length=11,choices=TYPE_SELECT, blank=True, null=True)
    # Delivery details
    country         = CountryField(blank_label='(select country)', blank=True)
    phone           = models.CharField(max_length=100, blank=True)
    town            = models.CharField(max_length=200, blank=True, null=True)
    estate          = models.CharField(max_length=200, blank=True, null=True)
    landmark        = models.CharField(max_length=200, blank=True, null=True)
    house_no        = models.CharField(max_length=200, blank=True, null=True)
    # User Status
    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    created         = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)
    
    objects         = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
        subject,
        message,
        'l@1.com',
        [self.email],
        fail_silently=False,
    )

    def __str__(self):
        return self.user_name
