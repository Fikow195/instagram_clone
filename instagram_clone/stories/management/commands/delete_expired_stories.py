from django.core.management.base import BaseCommand
from stories.models import Story
from django.utils import timezone

class Command(BaseCommand):
    help = 'Удаляет устаревшие сторис'

    def handle(self, *args, **kwargs):
        expired_stories = Story.objects.filter(expires_at__lte=timezone.now())
        for story in expired_stories:
            if story.image:
                story.image.delete(save=False)
            story.delete()
        self.stdout.write(self.style.SUCCESS('Удалены устаревшие сторис.'))
