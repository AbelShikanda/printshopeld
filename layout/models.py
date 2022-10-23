from django.db import models
from unicodedata import category
import uuid
from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField

# Create your models here.

class Socials(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    is_active = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "Socials"
        ordering = ('-name',)
    
    def __str__(self):
        return f'{self.name}'


class Layout(models.Model):
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField()
    
    class Meta:
        verbose_name_plural = "Layout"
        ordering = ('-created_at',)
    
    def __str__(self):
        return f'{self.name}'

class LayoutImage(models.Model):
    head_image = ResizedImageField(size=[1920, 920], crop=['middle', 'center'], default ='default_img', upload_to='headerimages')
    foot_image = ResizedImageField(size=[1920, 520], crop=['middle', 'center'], default ='default_img', upload_to='footerimages')
    deal_image = ResizedImageField(size=[1920, 620], crop=['middle', 'center'], default ='default_img', upload_to='dealsimages')
    bread_image = ResizedImageField(size=[1920, 620], crop=['middle', 'center'], default ='default_img', upload_to='breadcrumbimages')
    alt_text = models.CharField(max_length=100)
    is_header = models.BooleanField()
    is_deals = models.BooleanField()
    is_footer = models.BooleanField()
    is_breadcrumb = models.BooleanField()
    is_logo = models.BooleanField()
    
    layout = models.ForeignKey(Layout, on_delete=models.CASCADE, related_name="layout_image")
