from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipes, name='recipes'),
    path('search/', views.search, name='search'),
    path('recipe/<str:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('about/', views.about, name='about'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('api/recipes/', views.recipe_list_api, name='recipe_list_api'),
    path('api/cuisines/', views.cuisine_list_api, name='cuisine_list_api'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('meal_planner/', views.meal_planner, name='meal_planner'),
    path('saved_recipes/', views.saved_recipes, name='saved_recipes'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
]