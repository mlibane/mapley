import requests
from .models import MyTable
import os
from dotenv import load_dotenv
import json

response = requests.get(endpoint, params=params)
print(json.dumps(response.json(), indent=2))

load_dotenv()
api_key = os.getenv("SPOONACULAR_API_KEY")
endpoint = "https://api.spoonacular.com/recipes/complexSearch"

params = {
    "apiKey": api_key,
    "number": 100,
    "addRecipeInformation": True
}

response = requests.get(endpoint, params=params)
recipes = response.json()["data"]["results"]

for recipe in recipes:
    my_table_obj = MyTable(
        column1=recipe["title"],
        column2=recipe["id"],
        column3=recipe["readyInMinutes"],
        column4=recipe["servings"],
        column5=recipe["healthScore"],
        column6=recipe["cheap"],
        column7=recipe["vegan"],
        column8=recipe["vegetarian"],
        column9=recipe["glutenFree"],
        column10=recipe["dairyFree"],
        column11=", ".join(recipe["cuisines"]),
        column12=", ".join(recipe["dishTypes"]),
        column13=", ".join(recipe["diets"]),
        column14=recipe["summary"],
        column15=", ".join(recipe["analyzedInstructions"][0]["steps"]) if recipe["analyzedInstructions"] else "",
        column16=", ".join(recipe["extendedIngredients"]) if recipe["extendedIngredients"] else ""
    )
    my_table_obj.save()