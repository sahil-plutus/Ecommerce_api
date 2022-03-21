from django.contrib import admin
from django.urls import include, path
from . import views


urlpatterns = [
    path('products/', views.ProductView.as_view()),
    path('products/<int:pk>/', views.ProductView.as_view()),
    path('demo/', views.DemoView.as_view()),
    path('addproducts/', views.AddProductCsv.as_view()),
]
