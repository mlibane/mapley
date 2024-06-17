from django.shortcuts import render
from .models import Recipe
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def main(request):
    return render(request, 'recipes/main.html')

def recipes(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes}
    return render(request, 'recipes.html', context)

def search(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        recipes = []
    return render(request, 'recipes/search.html', {'recipes': recipes})