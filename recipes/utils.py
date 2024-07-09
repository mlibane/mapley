import requests
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.utils import timezone
import threading
import time
import string


BASE_URL = 'https://www.themealdb.com/api/json/v1/1/'
CACHE_TIMEOUT = 3600  # 1 hour
ALL_RECIPES_CACHE_KEY = 'all_recipes'

def search_recipes_api(query='', category=None, cuisine=None, page=1, per_page=9):
    all_recipes = get_all_recipes()
    
    # Filter recipes based on query, category, or cuisine
    if query:
        filtered_recipes = [r for r in all_recipes if query.lower() in r['strMeal'].lower()]
    elif category:
        filtered_recipes = [r for r in all_recipes if r['strCategory'].lower() == category.lower()]
    elif cuisine:
        filtered_recipes = [r for r in all_recipes if r['strArea'].lower() == cuisine.lower()]
    else:
        filtered_recipes = all_recipes

    # Sort recipes alphabetically
    filtered_recipes.sort(key=lambda x: x['strMeal'])

    total_results = len(filtered_recipes)
    total_pages = (total_results + per_page - 1) // per_page
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_recipes = filtered_recipes[start_index:end_index]

    return {
        'meals': paginated_recipes,
        'total_results': total_results,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages
    }
def get_all_recipes():
    all_recipes = cache.get(ALL_RECIPES_CACHE_KEY)
    if all_recipes is None:
        all_recipes = fetch_all_recipes()
        cache.set(ALL_RECIPES_CACHE_KEY, all_recipes, timeout=CACHE_TIMEOUT)
        threading.Thread(target=background_update_all_recipes).start()
    return all_recipes

def background_update_all_recipes():
    all_recipes = fetch_all_recipes()
    cache.set(ALL_RECIPES_CACHE_KEY, all_recipes, timeout=CACHE_TIMEOUT)

def fetch_all_recipes():
    all_recipes = []
    for letter in string.ascii_lowercase:
        url = f"{BASE_URL}search.php"
        params = {'f': letter}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            if data['meals']:
                all_recipes.extend(data['meals'])
        except requests.RequestException as e:
            print(f"API request failed for letter {letter}: {e}")
    return all_recipes

threading.Thread(target=background_update_all_recipes).start()

def fetch_recipes_with_rate_limit(url, params):
    recipes = []
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['meals']:
            recipes.extend(data['meals'])
        time.sleep(API_RATE_PERIOD / API_RATE_LIMIT)  # Respect rate limit
    except requests.RequestException as e:
        print(f"API request failed: {e}")
    return recipes

def background_cache_update(cache_key, category=None, cuisine=None):
    all_recipes = fetch_all_recipes(category, cuisine)
    cache.set(cache_key, all_recipes, timeout=CACHE_TIMEOUT)
    cache.set(f'{cache_key}_last_updated', timezone.now(), timeout=CACHE_TIMEOUT)

def get_recipe_by_id(recipe_id):
    cache_key = f'recipe_{recipe_id}'
    cached_recipe = cache.get(cache_key)
    
    if cached_recipe:
        return cached_recipe

    url = f'{BASE_URL}lookup.php?i={recipe_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['meals']:
            recipe = data['meals'][0]
            cache.set(cache_key, recipe, timeout=CACHE_TIMEOUT)
            return recipe
    except requests.RequestException as e:
        print(f"Error fetching recipe {recipe_id}: {str(e)}")
    return None

    
def search_recipes(query, offset=0, number=9):
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
