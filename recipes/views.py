from django.shortcuts import render
from django.db.models import Q
from .models import Recipe 
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Cuisine, Recipe, UserProfile, MealPlan
from .serializers import CuisineSerializer, RecipeSerializer, UserProfileSerializer, MealPlanSerializer


def home(request):
    cuisines = [
        {'name': 'AMERICAN', 'image': '/static/images/american.jpg'},
        {'name': 'KID FRIENDLY', 'image': '/static/images/kid-friendly.jpg'},
        {'name': 'ITALIAN', 'image': '/static/images/italian.jpg'},
        {'name': 'ASIAN', 'image': '/static/images/asian.jpg'},
        {'name': 'MEXICAN', 'image': '/static/images/mexican.jpg'},
        {'name': 'SOUTHERN & SOUL FOOD', 'image': '/static/images/southern.jpg'},
        {'name': 'FRENCH', 'image': '/static/images/french.jpg'},
        {'name': 'SOUTHWESTERN', 'image': '/static/images/southwestern.jpg'},
    ]
    recipes = Recipe.objects.all()[:5] 
    context = {
        'cuisines': cuisines,
        'recipes': recipes,
    }
    return render(request, 'home.html', context)

def recipes(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/recipes.html', context)

def search(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) | 
        Q(ingredients__icontains=query)
    )
    context = {
        'recipes': recipes,
        'query': query,
    }
    return render(request, 'search.html', context)

def main(request):
    context = {}
    return render(request, 'main.html', context)

def recipe_list_api(request):
    recipes = Recipe.objects.all()
    data = [{'id': recipe.id, 'title': recipe.title} for recipe in recipes]
    return JsonResponse(data, safe=False)

def cuisine_list_api(request):
    cuisines = [
        {'name': 'AMERICAN', 'image': '/static/images/american.jpg'},
        {'name': 'KID FRIENDLY', 'image': '/static/images/kid-friendly.jpg'},
    ]
    return JsonResponse(cuisines, safe=False)

class CuisineViewSet(viewsets.ModelViewSet):
    queryset = Cuisine.objects.all()
    serializer_class = CuisineSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer