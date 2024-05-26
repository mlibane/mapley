from django.shortcuts import render
from recipe_scrapers import scrape_me

# Home view
def home(request):
    return render(request, 'recipes/home.html')

# Search view
def search(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        scraper = scrape_me(url)
        recipe = {
            'title': scraper.title(),
            'ingredients': scraper.ingredients(),
            'instructions': scraper.instructions(),
            'image': scraper.image(),
        }
        return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})
    return render(request, 'recipes/search.html')

# Recipe detail view
def recipe_detail(request, id):
    # Placeholder for future implementation
    return render(request, 'recipes/recipe_detail.html')