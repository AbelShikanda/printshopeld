from unicodedata import category
import uuid
from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField

# code here

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
        # Manages and returns products thet are only active


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField()
    is_trending = models.BooleanField()
    
    class meta:
        verbose_name_plural = "Categories"
    
    def get_absolute_url(self):
        return reverse('shop:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class ProductType(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Product Type"
    
    def __str__(self):
        return f'{self.name} '

class Color(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    is_active = models.BooleanField()
    is_feature = models.BooleanField()
    is_trending = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    sku = models.CharField(max_length=50, unique=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    description = models.TextField()
    meta_title = models.CharField(max_length=100)
    meta_keywords = models.CharField(max_length=100)
    meta_description = models.TextField()
    slug = models.SlugField()
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="type")
    Color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="Color")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="size")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="material")
    
    objects = models.Manager()
    products = ProductManager()
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ('-created_at',)
    
    def get_absolute_url(self):
        return reverse('shop:sinlge_product_view', args=[self.slug])
    
    
    def __str__(self):
        return f'{self.name} '

class ProductImage(models.Model):
    feature_image = ResizedImageField(size=[300, 400], crop=['middle', 'center'], default ='default_img', upload_to='shopfeature')
    shop_image = ResizedImageField(size=[350, 450], crop=['middle', 'center'], default ='default_img', upload_to='shopshop')
    alt_text = models.CharField(max_length=100)
    is_active = models.BooleanField()
    is_smart_edit = models.BooleanField()
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
