from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Chat, Message

@login_required
def chat_list(request):
    chats = Chat.objects.filter(participants=request.user).order_by("name")
    users = User.objects.exclude(id=request.user.id).order_by("username")
    return render(
        request,
        "chat/chat_list.html",
        {"chats": chats, "users": users},
    )

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if not chat.participants.filter(id=request.user.id).exists():
        chat.participants.add(request.user)

    messages = chat.messages.select_related("sender").order_by("timestamp")
    participants = chat.participants.all().order_by("username")
    all_users = User.objects.all().order_by("username")
    return render(
        request,
        "chat/chat_detail.html",
        {
            "chat": chat,
            "messages": messages,
            "participants": participants,
            "all_users": all_users,
        },
    )

@login_required
def create_chat(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        participant_ids = request.POST.getlist("participants")

        if not name:
            return redirect("chat_list")

        try:
            chat = Chat.objects.create(name=name)
        except IntegrityError:
            return redirect("chat_list")
        chat.participants.add(request.user)

        if participant_ids:
            users = User.objects.filter(id__in=participant_ids)
            chat.participants.add(*users)

        return redirect("chat_detail", chat_id=chat.id)
    return redirect("chat_list")

@login_required
def send_message(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "POST" and chat.participants.filter(id=request.user.id).exists():
        text = request.POST.get("content", "").strip()
        file = request.FILES.get("image")

        if text or file:
            Message.objects.create(
                chat=chat,
                sender=request.user,
                content=text or None,
                image=file,
            )

    return redirect("chat_detail", chat_id=chat.id)


@login_required
def add_participant(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    if request.method == "POST" and chat.participants.filter(id=request.user.id).exists():
        user_id = request.POST.get("user_id")
        if user_id:
            user = get_object_or_404(User, id=user_id)
            chat.participants.add(user)

    return redirect("chat_detail", chat_id=chat.id)
