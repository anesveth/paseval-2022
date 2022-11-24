## PATH DEFINITIONS 
from django.urls import path
from . import views

urlpatterns = [
    path('strength/', views.viewStrength, name='view_strength'), 
    path('test-strength',views.Strength, name="post_password_input"),
    path('randomf',views.viewRandom, name="view_random"),
    path('generate-random',views.randomGeneration, name="generate_random_password"),
    path('personalizedf',views.viewPersonalizedg, name="view_personalized"),
    path('generate-personalized',views.personalizedGeneration, name="generate_random_password"),
    path('', views.Home, name='index')   
    
]


