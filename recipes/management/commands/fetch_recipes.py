# recipes/management/commands/fetch_recipes.py
import requests
from django.core.management.base import BaseCommand
from recipes.models import Recipe
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetch recipes from Spoonacular API and store them in the database'

    def handle(self, *args, **options):
        api_key = settings.SPOONACULAR_API_KEY
        url = f'https://api.spoonacular.com/recipes/random?number=100&apiKey={api_key}'
        response = requests.get(url)
        data = response.json()
        recipes = data.get('recipes', [])

        for recipe_data in recipes:
            recipe = Recipe(
                title=recipe_data['title'],
                ingredients="\n".join([ingredient['original'] for ingredient in recipe_data['extendedIngredients']]),
                instructions=recipe_data.get('instructions', ''),
                source_url=recipe_data.get('sourceUrl', '')
            )
            recipe.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully saved recipe: {recipe.title}'))
