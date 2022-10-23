from email.policy import default
from django.db import models
from django.urls import reverse
from django_resized import ResizedImageField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField()
    
    class meta:
        verbose_name_plural = "Categories"
    
    def get_absolute_url(self):
        return reverse('blog:category_list', args=[self.slug])

    def __str__(self):
        return self.name

class Blog(models.Model):
    is_active = models.BooleanField()
    is_feature = models.BooleanField()
    title = models.CharField(max_length=100)
    intro = models.TextField()
    body = models.TextField()
    quote = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateField(auto_now_add=True, editable=False)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    
    class Meta:
        verbose_name_plural = "Blogs"
        ordering = ('-created_at',)

    
    def get_absolute_url(self):
        return reverse('blog:blog_single_view', args=[self.slug])
    
    def __str__(self):
        return self.title

class BlogImage(models.Model):
    large_image = ResizedImageField(size=[1920, 900], crop=['middle', 'center'], default ='default_img', upload_to='bloglarge')
    small_image = ResizedImageField(size=[300, 400], crop=['middle', 'center'], default ='default_img', upload_to='blogsmall')
    lead_image = ResizedImageField(size=[380, 470], crop=['middle', 'center'], default ='default_img', upload_to='blogsmall')
    alt_text = models.CharField(max_length=100)
    is_lead = models.BooleanField()
    is_active = models.BooleanField()
    is_heading = models.BooleanField()
    is_feature = models.BooleanField()
    is_footing = models.BooleanField()
    
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_image")