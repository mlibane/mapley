"""
URL configuration for mapley project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from recipes import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from allauth.account.views import LoginView, SignupView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('admin/', admin.site.urls),
    path('recipes/', views.recipes, name='recipes'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('api/recipes/', views.recipe_list_api, name='recipe_list_api'),
    path('api/cuisines/', views.cuisine_list_api, name='cuisine_list_api'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', SignupView.as_view(template_name='signup.html'), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('recipes.urls')),
    path('accounts/', include('allauth.urls')),
]