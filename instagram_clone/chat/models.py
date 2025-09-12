from django.db import models
from django.contrib.auth.models import User
from .storage_backends import AzureMediaStorage

class Chat(models.Model):
    name = models.CharField(max_length=255)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # Для Azure Blob
    timestamp = models.DateTimeField(auto_now_add=True)

    # class Message(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField(blank=True, null=True)
#     image_url = models.URLField(blank=True, null=True)  # Здесь будем хранить ссылку на Blob
#     timestamp = models.DateTimeField(auto_now_add=True)

# class Chat(models.Model):
#     name = models.CharField(max_length=100, blank=True)  # для группового чата
#     participants = models.ManyToManyField(User, related_name='chats')
# 
#     def __str__(self):
#         return self.name if self.name else f"Chat {self.id}"

    # class Message(models.Model):
#     chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"
