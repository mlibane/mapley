import requests
from django.conf import settings
from django.core.cache import cache
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

def search_recipes_api(query, category=None, offset=0, number=10):
    base_url = settings.THEMEALDB_API_URL
    
    if category:
        url = f"{base_url}filter.php"
        params = {'c': category}
    elif query:
        url = f"{base_url}search.php"
        params = {'s': query}
    else:
        url = f"{base_url}random.php"
        params = {}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        meals = data.get('meals', [])
        total_results = len(meals)
        
        # Apply pagination
        paginated_meals = meals[offset:offset+number]
        
        return {
            'hits': paginated_meals,
            'count': total_results
        }
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None
    
def search_recipes(query, offset=0, number=10):
    url = f"{BASE_URL}search.php"
    params = {'s': query}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        meals = data['meals'] or []
        return {
            'hits': meals[offset:offset+number],
            'count': len(meals)
        }
    return None 

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
        {'name': 'Breakfast', 'link': '/recipes?category=breakfast'},
        {'name': 'Lunch', 'link': '/recipes?category=lunch'},
        {'name': 'Dinner', 'link': '/recipes?category=dinner'},
        {'name': 'Desserts', 'link': '/recipes?category=desserts'},
        {'name': 'Vegetarian', 'link': '/recipes?category=vegetarian'},
        {'name': 'Quick & Easy', 'link': '/recipes?category=quick-easy'}
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
    url = f"{BASE_URL}lookup.php"
    params = {'i': recipe_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['meals'][0] if data['meals'] else None
    return None

def get_featured_recipes(count=6):
    base_url = settings.THEMEALDB_API_URL
    featured_recipes = []

    for _ in range(count):
        try:
            response = requests.get(f"{base_url}random.php")
            response.raise_for_status()
            data = response.json()
            if data['meals'] and len(data['meals']) > 0:
                featured_recipes.append(data['meals'][0])
        except requests.RequestException as e:
            print(f"Error fetching recipe: {e}")

    return featured_recipes

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