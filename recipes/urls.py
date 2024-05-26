from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('recipies/', views.recipes, name='recipies'),
    path('recipies/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),    
]