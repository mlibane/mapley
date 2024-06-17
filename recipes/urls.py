from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('recipes/', views.recipes, name='recipes'),
    path('search/', views.search, name='search')
]
