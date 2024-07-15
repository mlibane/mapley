from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cuisine, Recipe, UserProfile, MealPlan 
from django.http import Http404, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from supabase import create_client, Client
from rest_framework import generics
from .models import Recipe
from .serializers import RecipeSerializer
import concurrent.futures
import random
from .utils import (
    get_cuisines,
    get_popular_recipes,
    search_recipes,
    get_recipe_by_id,
    get_popular_categories,
    search_recipes_api,
    get_featured_recipes,
)
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, RecipeForm
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import logging

logger = logging.getLogger(__name__)


def get_popular_categories():
    return [
        {'name': 'Breakfast', 'link': '/recipes?category=Breakfast'},
        {'name': 'Chicken', 'link': '/recipes?category=Chicken'},
        {'name': 'Dessert', 'link': '/recipes?category=Dessert'},
        {'name': 'Pasta', 'link': '/recipes?category=Pasta'},
        {'name': 'Seafood', 'link': '/recipes?category=Seafood'},
        {'name': 'Vegetarian', 'link': '/recipes?category=Vegetarian'}
    ]

def home(request):
    context = {
        'sidebar_items': [
            {'name': 'Meal Planning', 'link': '/meal-planning', 'icon': 'meal-planning-icon.png'},
            {'name': 'My Feed', 'link': '/my-feed', 'icon': 'feed-icon.png'},
            {'name': 'Browse', 'link': '/browse', 'icon': 'browse-icon.png'},
            {'name': 'Pro Recipes', 'link': '/pro-recipes', 'icon': 'pro-icon.png'},
            {'name': 'Guided Recipes', 'link': '/guided-recipes', 'icon': 'guided-icon.png'},
            {'name': 'Articles', 'link': '/articles', 'icon': 'article-icon.png'},
            {'name': 'Saved Recipes', 'link': '/saved-recipes', 'icon': 'saved-icon.png'},
            {'name': 'More Tools', 'link': '/more-tools', 'icon': 'tools-icon.png'},
        ],
        'featured_recipes': get_featured_recipes(),
        'cuisines': get_cuisines(),
        'popular_categories': get_popular_categories(),
    }
    return render(request, 'home.html', context)

@api_view(['GET'])
def recipe_list_api(request):
    recipes = get_featured_recipes()
    return Response(recipes)

@api_view(['GET'])
def cuisine_list_api(request):
    cuisines = get_cuisines()
    return Response(cuisines)

@cache_page(60)  # Cache this view for 1 minute
def recipes(request):
    category = request.GET.get('category')
    cuisine = request.GET.get('cuisine')
    query = request.GET.get('q')
    page = int(request.GET.get('page', 1))
    recipes_per_page = 9

    recipes_data = search_recipes_api(query=query, category=category, cuisine=cuisine, page=page, per_page=recipes_per_page)

    # Calculate pagination range
    total_pages = recipes_data['total_pages']
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 3:
            page_range = range(1, 6)
        elif page > total_pages - 3:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(page - 2, page + 3)

    context = {
        'recipes': recipes_data['meals'],
        'category': category,
        'cuisine': cuisine,
        'query': query,
        'page': page,
        'page_range': page_range,
        'total_pages': total_pages,
        'total_results': recipes_data['total_results'],
    }
    
    return render(request, 'recipes.html', context)

def recipe_detail(request, recipe_id):
    try:
        url = f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data['meals']:
            logger.error(f"No recipe found for id: {recipe_id}")
            raise Http404("Recipe not found")
        
        recipe = data['meals'][0]
        logger.debug(f"Recipe data: {recipe}")
        
        # Extract ingredients and measures
        ingredients = []
        for i in range(1, 21):  # TheMealDB provides up to 20 ingredients
            ingredient = recipe.get(f'strIngredient{i}')
            measure = recipe.get(f'strMeasure{i}')
            if ingredient and ingredient.strip():
                ingredients.append({
                    'name': ingredient,
                    'measure': measure
                })
        
        # Filter out empty or numbered-only instructions
        instructions = []
        for step in recipe['strInstructions'].split('\r\n'):
            step = step.strip()
            if step and not step.isdigit() and not step.startswith('.'):
                instructions.append(step)
        
        context = {
            'recipe': recipe,
            'ingredients': ingredients,
            'instructions': instructions,
        }
        return render(request, 'recipe_detail.html', context)
    except requests.RequestException as e:
        logger.error(f"API request failed for recipe {recipe_id}: {str(e)}")
        return render(request, 'error.html', {'error': "Failed to fetch recipe data. Please try again later."})
    except Exception as e:
        logger.error(f"Unexpected error in recipe_detail view: {str(e)}")
        return render(request, 'error.html', {'error': str(e)})

def search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    results_per_page = 9
    
    if not query:
        return render(request, 'search.html')
    
    try:
        url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={query}'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        all_recipes = data.get('meals', [])
        total_results = len(all_recipes)
        
        # Simple pagination
        start = (page - 1) * results_per_page
        end = start + results_per_page
        recipes = all_recipes[start:end]
        
        context = {
            'recipes': recipes,
            'query': query,
            'page': page,
            'total_results': total_results,
            'total_pages': (total_results + results_per_page - 1) // results_per_page,
        }
        return render(request, 'search.html', context)
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        messages.error(request, "An error occurred while searching. Please try again later.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        messages.error(request, "An unexpected error occurred. Please try again.")
    
    return render(request, 'search.html', {'query': query})

def recipes_by_category(request, category):
    page = int(request.GET.get('page', 1))
    recipes_per_page = 9
    recipes_data = search_recipes_api(category=category, page=page, per_page=recipes_per_page)
    
    # Calculate pagination range
    total_pages = recipes_data['total_pages']
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 3:
            page_range = range(1, 6)
        elif page > total_pages - 3:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(page - 2, page + 3)
    
    context = {
        'recipes': recipes_data['meals'],
        'category': category,
        'page': page,
        'page_range': page_range,
        'total_pages': total_pages,
        'total_results': recipes_data['total_results'],
    }
    return render(request, 'recipes.html', context)

def recipes_by_cuisine(request, cuisine):
    page = int(request.GET.get('page', 1))
    recipes_per_page = 9
    recipes_data = search_recipes_api(cuisine=cuisine, page=page, per_page=recipes_per_page)
    
    # Calculate pagination range
    total_pages = recipes_data['total_pages']
    if total_pages <= 5:
        page_range = range(1, total_pages + 1)
    else:
        if page <= 3:
            page_range = range(1, 6)
        elif page > total_pages - 3:
            page_range = range(total_pages - 4, total_pages + 1)
        else:
            page_range = range(page - 2, page + 3)
    
    context = {
        'recipes': recipes_data['meals'],
        'cuisine': cuisine,
        'page': page,
        'page_range': page_range,
        'total_pages': total_pages,
        'total_results': recipes_data['total_results'],
    }
    return render(request, 'recipes.html', context)

def search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) >= 3:
        suggestions = Recipe.objects.filter(title__icontains=query)[:5]
        return JsonResponse({'suggestions': [recipe.title for recipe in suggestions]})
    return JsonResponse({'suggestions': []})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')  

@method_decorator(cache_page(60 * 15), name='dispatch')
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        cuisine = self.request.GET.get('cuisine')
        query = self.request.GET.get('q')
        return search_recipes_api(query=query, category=category, cuisine=cuisine)

class RecipeListAPIView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_fields = ['category', 'cuisine']
    search_fields = ['title', 'description']

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    context_object_name = 'recipe'

class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'create_recipe.html'
    success_url = reverse_lazy('recipes')
                        
def main(request):
    context = {}
    return render(request, 'main.html', context)

def my_recipes(request):
    context = {}
    return render(request, 'my_recipes.html', context)

def meal_planner(request):
    context = {}
    return render(request, 'meal_planner.html', context)

def saved_recipes(request):
    context = {}
    return render(request, 'saved_recipes.html', context)

def profile(request):
    context = {}
    return render(request, 'profile.html', context)

def about(request):
    return render(request, 'about.html')

def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes')
    else:
        form = RecipeForm()
    return render(request, 'create_recipe.html', {'form': form})

def verification_sent(request):
    return render(request, 'verification_sent.html')

def email_confirmation(request):
    return render(request, 'email_confirmation.html')

def invalid_token(request):
    return render(request, 'invalid_token.html')

def error_404(request, exception):
    return render(request, 'error.html', {'error_message': 'Page not found'}, status=404)

def error_500(request):
    return render(request, 'error.html', {'error_message': 'Server error'}, status=500)