from django.shortcuts import render, redirect, get_object_or_404
from .models import Chat, Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        chat = get_object_or_404(Chat, id=chat_id)
        text = request.POST.get('text', '')
        image = request.FILES.get('image')
        Message.objects.create(chat=chat, sender=request.user, text=text, image=image)
    return redirect('chat_detail', chat_id=chat_id)
