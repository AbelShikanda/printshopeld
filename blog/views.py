from django.shortcuts import get_object_or_404, render
from .models import *

# Create your views here.

def blog_view (request):
    blogs =  Blog.objects.prefetch_related("blog_image").filter(is_active=True,)
    
    context = {
        'blogs' : blogs
        }   
    return render(request, 'printshop/blog.html', context);


def blog_single_view (request, slug):
    blog = get_object_or_404(Blog, slug=slug, is_active=True)
    
    context  = {
        'blog' : blog
        }  
    return render(request, 'printshop/blog_single.html', context);

def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    blogs = Blog.objects.filter(category=category)
    
    context  = {
        'category' : category,
        'blogs' : blogs,
        }  
    return render(request, 'printshop/blog_category.html', context);

def catagory_view (request):
    category = Blog.objects.all()
    
    context  = {
        'category' : category
        }  
    return render(request, 'printshop/blog_category.html', context);