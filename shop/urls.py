
from django.urls import path
from . import views

app_name = 'shop'
urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('catalog', views.catalog_view, name='catalog_view'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('single_product/<slug:slug>/', views.sinlge_product_view, name='sinlge_product_view'),
]