from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('create/', views.story_create, name='story_create'),  # <- вот эта строка!
]
