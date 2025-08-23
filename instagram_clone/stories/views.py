from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Story
from .forms import StoryForm

@login_required
def add_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect("stories:story_list")
    else:
        form = StoryForm()
    return render(request, "stories/add_story.html", {"form": form})

@login_required
def story_list(request):
    expired_time = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(created_at__gte=expired_time).order_by("-created_at")
    return render(request, "stories/story_list.html", {"stories": stories})
