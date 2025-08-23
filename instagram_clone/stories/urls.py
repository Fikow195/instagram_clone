from django.urls import path
from . import views

app_name = "stories"

urlpatterns = [
    path("", views.story_list, name="story_list"),
    path("add/", views.add_story, name="add_story"),
]
