
from datetime import timedelta
from itertools import product
from time import timezone
from django.shortcuts import redirect, render, get_object_or_404

from blog.models import Blog

from . models import *


# Create your views here.

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    
    context  = {
        'category' : category,
        'products' : products,
        }  
    return render(request, 'printshop/category.html', context);

def home_view (request):
    trending = Product.objects.filter(is_active=True, is_trending=True)
    feature = Product.objects.filter(is_active=True, is_feature=True)
    blogs = Blog.objects.filter(is_active=True, is_feature=True, pk__lt=10)
    
    context  = {
        'trending' : trending,
        'feature' : feature,
        'blogs' : blogs,
        } 
    return render(request, 'printshop/home.html', context);

def catalog_view (request):
    catalogs = Product.objects.all()
    
    context  = {
        'catalogs' : catalogs
        }  
    return render(request, 'printshop/catalog.html', context);

def sinlge_product_view (request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    context  = {
        'product' : product
        }   
    return render(request, 'printshop/single_product.html', context);

def compare_view (request):   
    return render(request, 'printshop/compare.html', {});

def track_view (request):   
    return render(request, 'printshop/track.html', {});

def wishlist_view (request):   
    return render(request, 'printshop/wishlist.html', {});

def faqs_view (request):   
    return render(request, 'printshop/faqs.html', {});

def contact_view (request):   
    return render(request, 'printshop/contact.html', {});

