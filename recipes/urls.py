from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('recipes/', views.recipes, name='recipes'),
    path('search/', views.search, name='search'),
    path('api/recipes/', views.recipe_list_api, name='recipe_list_api'),
    path('api/cuisines/', views.cuisine_list_api, name='cuisine_list_api'),
]

