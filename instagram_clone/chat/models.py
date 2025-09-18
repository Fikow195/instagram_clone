from django.contrib.auth.models import User
from django.db import models

from .storage_backends import get_media_storage


from .storage_backends import AzureMediaStorage


class Chat(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name="chats", blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(
        storage=get_media_storage(), upload_to="chat_images/", blank=True, null=True

        storage=AzureMediaStorage(), upload_to="chat_images/", blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("timestamp",)

    def __str__(self) -> str:
        preview = self.content or "📷"
        return f"{self.sender.username}: {preview[:20]}"
