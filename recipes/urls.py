from django.urls import path, include
from . import views
from .views import RecipeListAPIView, CreateRecipeView

recipe_patterns = [
    path('', RecipeListAPIView.as_view(), name='recipes'),
    path('category/<str:category>/', views.recipes_by_category, name='recipes_by_category'),
    path('cuisine/<str:cuisine>/', views.recipes_by_cuisine, name='recipes_by_cuisine'),
    path('recipes/<str:recipe_id>-<str:recipe_name>/', views.recipe_detail, name='recipe_detail'),
]

api_patterns = [
    path('recipes/', views.recipe_list_api, name='recipe_list_api'),
    path('cuisines/', views.cuisine_list_api, name='cuisine_list_api'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', include(recipe_patterns)),
    path('api/', include(api_patterns)),
    path('recipes/<str:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('search/', views.search, name='search'),
    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('about/', views.about, name='about'),
    path('my_recipes/', views.my_recipes, name='my_recipes'),
    path('meal_planner/', views.meal_planner, name='meal_planner'),
    path('saved_recipes/', views.saved_recipes, name='saved_recipes'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('create/', CreateRecipeView.as_view(), name='create_recipe'),
]