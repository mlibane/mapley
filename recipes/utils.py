import requests
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
import random


BASE_URL = 'https://www.themealdb.com/api/json/v1/1/'


def get_recipe_from_api(recipe_id):
    cache_key = f'recipe_{recipe_id}'
    cached_recipe = cache.get(cache_key)
    if cached_recipe:
        return cached_recipe

    app_id = settings.EDAMAM_RECIPE_APP_ID
    app_key = settings.EDAMAM_RECIPE_API_KEY
    url = f'https://api.edamam.com/api/recipes/v2/{recipe_id}'
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'type': 'public'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        recipe_data = response.json()
        cache.set(cache_key, recipe_data, timeout=3600)  # Cache for 1 hour
        return recipe_data
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None

def search_recipes_api(query='', category=None):
    cache_key = f'all_recipes_{category}_{query}'
    cached_recipes = cache.get(cache_key)
    
    if cached_recipes:
        return cached_recipes

    base_url = settings.THEMEALDB_API_URL
    
    if category:
        url = f"{base_url}filter.php"
        params = {'c': category}
    elif query:
        url = f"{base_url}search.php"
        params = {'s': query}
    else:
        url = f"{base_url}search.php"
        params = {'s': ''}  # This will return all meals

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        meals = data.get('meals', [])
        
        # Fetch detailed information for each recipe
        detailed_meals = [get_recipe_by_id(meal['idMeal']) for meal in meals]
        
        result = {
            'meals': detailed_meals,
            'total_results': len(detailed_meals)
        }
        
        cache.set(cache_key, result, timeout=3600)  # Cache for 1 hour
        return result
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return {'meals': [], 'total_results': 0}
    
def search_recipes(query, offset=0, number=10):
    cache_key = f'search_results_{query}_{offset}_{number}'
    cached_results = cache.get(cache_key)

    if cached_results is not None:
        return cached_results

    # First, try an exact match
    exact_matches = Recipe.objects.filter(
        Q(title__icontains=query) | 
        Q(ingredients__icontains=query) |
        Q(instructions__icontains=query)
    )

    # If no exact matches, use full-text search
    if not exact_matches:
        search_vector = SearchVector('title', weight='A') + \
                        SearchVector('ingredients', weight='B') + \
                        SearchVector('instructions', weight='C')
        search_query = SearchQuery(query)
        results = Recipe.objects.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gte=0.3).order_by('-rank')
    else:
        results = exact_matches

    total_results = results.count()
    paginated_results = results[offset:offset+number]

    cache.set(cache_key, results, timeout=3600)  # Cache for 1 hour
    return {
        'results': paginated_results,
        'total_results': total_results
    }

def get_cuisines():
    cache_key = 'cuisines'
    cached_cuisines = cache.get(cache_key)
    if cached_cuisines:
        return cached_cuisines

    url = f"{BASE_URL}list.php?a=list"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        cuisines = [{'name': cuisine['strArea'], 'image': f"https://www.themealdb.com/images/category/{cuisine['strArea'].lower()}.png"} for cuisine in data['meals']]
        cache.set(cache_key, cuisines, timeout=3600)  # Cache for 1 hour
        return cuisines
    return []

def get_popular_categories():
    return [
        {'name': 'Breakfast', 'link': '/recipes/?category=Breakfast'},
        {'name': 'Chicken', 'link': '/recipes/?category=Chicken'},
        {'name': 'Dessert', 'link': '/recipes/?category=Dessert'},
        {'name': 'Pasta', 'link': '/recipes/?category=Pasta'},
        {'name': 'Seafood', 'link': '/recipes/?category=Seafood'},
        {'name': 'Vegetarian', 'link': '/recipes/?category=Vegetarian'}
    ]

def get_popular_recipes(count=8):
    cache_key = 'popular_recipes'
    cached_recipes = cache.get(cache_key)
    if cached_recipes:
        return cached_recipes

    url = f"{BASE_URL}random.php"
    recipes = []
    for _ in range(count):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['meals']:
                recipes.append(data['meals'][0])
    
    cache.set(cache_key, recipes, timeout=3600)  # Cache for 1 hour
    return recipes

def get_recipe_by_id(recipe_id):
    cache_key = f'recipe_{recipe_id}'
    cached_recipe = cache.get(cache_key)
    
    if cached_recipe:
        return cached_recipe

    url = f'{settings.THEMEALDB_API_URL}lookup.php?i={recipe_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['meals']:
            recipe = data['meals'][0]
            cache.set(cache_key, recipe, timeout=3600)  # Cache for 1 hour
            return recipe
    except requests.RequestException as e:
        print(f"Error fetching recipe {recipe_id}: {str(e)}")
    return None

def get_featured_recipes(count=6):
    cache_key = 'featured_recipes'
    featured_recipes = cache.get(cache_key)

    if featured_recipes is None:
        featured_recipes = []
        for _ in range(count):
            try:
                response = requests.get(f"{settings.THEMEALDB_API_URL}random.php")
                response.raise_for_status()
                data = response.json()
                if data['meals'] and len(data['meals']) > 0:
                    featured_recipes.append(data['meals'][0])
            except requests.RequestException as e:
                print(f"Error fetching recipe: {e}")

        # Cache the featured recipes for 1 hour
        cache.set(cache_key, featured_recipes, 60 * 60)

    return featured_recipes[:count]

def get_personalized_recipes(num_recipes=10):
    cache_key = f'personalized_recipes_{num_recipes}'
    cached_recipes = cache.get(cache_key)
    if cached_recipes:
        return cached_recipes

    app_id = settings.EDAMAM_RECIPE_APP_ID
    app_key = settings.EDAMAM_RECIPE_API_KEY
    url = 'https://api.edamam.com/api/recipes/v2'
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'type': 'public',
        'random': 'true',
        'field': ['label', 'image', 'source', 'url', 'yield', 'dietLabels', 'healthLabels', 'cautions', 'ingredientLines', 'calories', 'totalTime'],
        'to': num_recipes
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        recipes = response.json()['hits']
        
        personalized_recipes = [
            {
                'title': recipe['recipe']['label'],
                'image': recipe['recipe']['image'],
                'description': f"A {', '.join(recipe['recipe']['dietLabels'])} dish from {recipe['recipe']['source']}",
                'id': recipe['recipe']['uri'].split('_')[-1]
            }
            for recipe in recipes
        ]
        
        # Cache the results for 1 hour
        cache.set(cache_key, personalized_recipes, timeout=3600)
        
        return personalized_recipes
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return []


def get_food_database_info(food_id):
    app_id = settings.EDAMAM_FOOD_DATABASE_APP_ID
    app_key = settings.EDAMAM_FOOD_DATABASE_API_KEY
    url = f'https://api.edamam.com/api/food-database/v2/parser'
    params = {
        'app_id': app_id,
        'app_key': app_key,
        'ingr': food_id
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        food_data = response.json()
        return food_data
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None

def get_nutrition_analysis(ingredients):
    app_id = settings.EDAMAM_NUTRITION_APP_ID
    app_key = settings.EDAMAM_NUTRITION_API_KEY
    url = 'https://api.edamam.com/api/nutrition-details'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'ingr': ingredients
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, params={'app_id': app_id, 'app_key': app_key})
        response.raise_for_status()
        nutrition_data = response.json()
        return nutrition_data
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None