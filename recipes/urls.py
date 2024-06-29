from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('recipes/', views.recipes, name='recipes'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('api/recipes/', views.recipe_list_api, name='recipe_list_api'),
    path('api/cuisines/', views.cuisine_list_api, name='cuisine_list_api'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('verification-sent/', views.verification_sent, name='verification_sent'),
    path('email-verified/', views.email_verified, name='email_verified'),
    path('invalid-token/', views.invalid_token, name='invalid_token'),
]