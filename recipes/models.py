from django.db import models
from django.contrib.postgres.search import SearchVectorField

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.IntegerField(null=True)
  joined_date = models.DateField(null=True)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    search_vector = SearchVectorField(null=True)

    def save(self, *args, **kwargs):
        self.search_vector = SearchVector('title', 'description', 'ingredients', 'instructions')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title