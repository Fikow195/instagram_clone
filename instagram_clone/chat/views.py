from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Chat, Message

@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'chat/chat_list.html', {'chats': chats})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat).order_by('timestamp')
    return render(request, 'chat/chat_detail.html', {'chat': chat, 'messages': messages})

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "POST":
        content = request.POST.get("text", "")  # получаем из формы поле text
        image = request.FILES.get("image")

        if content or image:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=content,  # сохраняем именно в content
                image=image
            )

    return redirect("chat_detail", chat_id=chat.id)

