from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.conf import settings
from azure.storage.blob import BlobServiceClient

@login_required
def chat_list(request):
    chats = Chat.objects.all()
    return render(request, "chat/chat_list.html", {"chats": chats})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.all().order_by("timestamp")
    return render(request, "chat/chat_detail.html", {"chat": chat, "messages": messages})

@login_required
def create_chat(request):
    if request.method == "POST":
        chat = Chat.objects.create()
        return redirect("chat_detail", chat_id=chat.id)
    return redirect("chat_list")

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "POST":
        text = request.POST.get("text")
        file = request.FILES.get("image")
        image_url = None

        if file:
            # Загружаем файл в Azure Blob и получаем публичную ссылку
            image_url = upload_image_to_blob(file)

        if text or image_url:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=text,
                image_url=image_url
            )

    return redirect("chat_detail", chat_id=chat.id)


def upload_image_to_blob(file):
    """
    Загружает файл в Azure Blob Storage и возвращает публичную ссылку
    """
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client("chat-media")

    blob_client = container_client.get_blob_client(file.name)
    blob_client.upload_blob(file, overwrite=True)

    # Формируем публичный URL
    url = f"https://{settings.stoga4}.blob.core.windows.net/chat-media/{file.name}"
    return url
