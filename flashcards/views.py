from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render

from .models import Conversation, Message


@login_required(login_url="/accounts/login/")
def chat_interface(request):
    messages = []

    if request.user.is_authenticated:
        if conversation_id := request.session.get("conversation_id"):
            conversation = Conversation.objects.get(user=request.user, id=conversation_id)
        else:
            conversation = Conversation.objects.create(user=request.user)
            conversation.save()
            request.session["conversation_id"] = conversation.id

        for msg in conversation.messages.all():
            messages.append(msg)
    return render(request, "chat_interface.html", {"messages": messages})


@login_required(login_url="/accounts/login/")
def list_user_conversations(request):
    """This endpoint will list the user conversations"""
    conversations = list(Conversation.objects.filter(user=request.user).all())
    data = serialize("json", conversations)
    return JsonResponse(data, safe=False)


def api_chat(request):
    # Create a new conversation if one doesn't exist
    if "conversation_id" not in request.session:
        conversation = Conversation.objects.create(user=request.user)
        request.session["conversation_id"] = conversation.id
    else:
        conversation = Conversation.objects.get(user=request.user, id=request.session["conversation_id"])

    # Save user message
    user_input = request.POST.get("text").strip()
    assert isinstance(user_input, str), f"Expected user to enter a string instead got: {user_input}"
    Message.objects.create(conversation=conversation, text=user_input, role="user")

    # TODO: Get chatbot's response here
    # ToDo: ensure it is whitespace stripped
    bot_response = "Hello, this is a placeholder response."

    # Save bot message
    Message.objects.create(conversation=conversation, text=bot_response, role="assistant")

    return JsonResponse({"text": bot_response})


def chat_room(request):
    return render(request, "chat/index.html")


def room(request, room_name: str):
    return render(request, "chat/room.html", {"room_name": room_name})
