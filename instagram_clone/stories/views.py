from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Story
from .forms import StoryForm

@login_required
def story_list(request):
    stories = Story.objects.all().order_by('-created_at')
    return render(request, 'stories/story_list.html', {'stories': stories})

@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('story_list')
    else:
        form = StoryForm()
    return render(request, 'stories/story_form.html', {'form': form})
