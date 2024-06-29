from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Recipe 
from django.http import JsonResponse
from django.core.paginator import Paginator
from .utils import (
    get_cuisines,
    get_popular_recipes,
    search_recipes,
    get_recipe_by_id,
    get_popular_categories,
)
from .models import Cuisine, Recipe, UserProfile, MealPlan
from .serializers import CuisineSerializer, RecipeSerializer, UserProfileSerializer, MealPlanSerializer
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, RecipeForm
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.text import slugify

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
        'featured_recipes': get_popular_recipes(),
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

def recipes(request):
    all_recipes = Recipe.objects.all().order_by('-created_at')
    paginator = Paginator(all_recipes, 12)  # Show 12 recipes per page
    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)
    
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes.html', context)

def search(request):
    query = request.GET.get('q', '')
    page = int(request.GET.get('page', 1))
    
    if not query:
        messages.error(request, "Please enter a search term.")
        return render(request, 'search.html')
    
    try:
        results = search_recipes(query, offset=(page-1)*10, number=10)
        
        if results is None:
            messages.error(request, "An error occurred while searching for recipes. Please try again later.")
            recipes = []
            total_results = 0
        else:
            recipes = results['hits']
            total_results = results['count']

        context = {
            'recipes': recipes,
            'query': query,
            'page': page,
            'total_results': total_results,
        }
        return render(request, 'search.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'error.html', status=500)

def main(request):
    context = {}
    return render(request, 'main.html', context)

def recipe_detail(request, recipe_id):
    try:
        recipe = get_recipe_by_id(recipe_id)
        if recipe is None:
            messages.error(request, "Recipe not found.")
            return render(request, 'error.html', status=404)
        
        context = {
            'recipe': recipe,
        }
        return render(request, 'recipe_detail.html', context)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'error.html', status=500)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile.objects.create(user=user)
            
            # Send verification email
            subject = 'Verify your email'
            message = f'Click the link to verify your email: {request.build_absolute_uri(reverse("verify_email", args=[str(profile.verification_token)]))})'
            send_mail(subject, message, 'from@example.com', [user.email])
            
            return redirect('verification_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def verify_email(request, token):
    try:
        profile = UserProfile.objects.get(verification_token=token)
        profile.email_verified = True
        profile.save()
        return redirect('email_verified')
    except UserProfile.DoesNotExist:
        return redirect('invalid_token')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                if hasattr(user, 'userprofile') and user.userprofile.email_verified:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Please verify your email before logging in.')
            else:
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


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

def email_verified(request):
    return render(request, 'email_verified.html')

def invalid_token(request):
    return render(request, 'invalid_token.html')


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

def error_404(request, exception):
    return render(request, 'error.html', {'error_message': 'Page not found'}, status=404)

def error_500(request):
    return render(request, 'error.html', {'error_message': 'Server error'}, status=500)