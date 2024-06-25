from django.db import models
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True)
    joined_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class Cuisine(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cuisines/')

class Recipe(models.Model):
    title = models.CharField(max_length=200, default='Untitled')
    slug = models.SlugField(unique=True, default='')
    description = models.TextField(default='')
    prep_time = models.PositiveIntegerField(help_text="Time to prepare the recipe in minutes.", default=0)
    cook_time = models.PositiveIntegerField(help_text="Time to cook the recipe in minutes.", default=0)
    total_time = models.PositiveIntegerField(help_text="Total time to make the recipe in minutes.", default=0)
    serves = models.PositiveIntegerField(help_text="Number of people the recipe serves.", default=1)
    difficulty = models.CharField(max_length=50, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ], default='easy')
    cuisine = models.CharField(max_length=100, default='')
    category = models.CharField(max_length=100, default='General')
    ingredients = models.TextField(default='')
    instructions = models.TextField(default='')
    tags = models.ManyToManyField('Tag')
    image = models.ImageField(upload_to='recipes', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    search_vector = SearchVectorField(null=True)

    def generate_slug(self):
        return slugify(self.title)[:100]

    class Meta:
        indexes = [
            models.Index(fields=['search_vector'], name='search_vector_idx'),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        self.search_vector = SearchVector('title', 'description', 'ingredients', 'instructions')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cuisines = models.ManyToManyField(Cuisine)
    saved_recipes = models.ManyToManyField(Recipe)

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    recipes = models.ManyToManyField(Recipe)