# Generated by Django 5.0.6 on 2024-07-03 22:39

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_recipe_cooking_time'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='recipe',
            name='search_vector_idx',
        ),
        migrations.AddIndex(
            model_name='recipe',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='recipes_rec_search__ce256b_gin'),
        ),
    ]
