from django.shortcuts import render

def chat_interface(request):
    return render(request, 'chat_interface.html')

from django.http import JsonResponse
from .models import Conversation, Message

def api_chat(request):
    # Create a new conversation if one doesn't exist
    if 'conversation_id' not in request.session:
        conversation = Conversation.objects.create()
        request.session['conversation_id'] = conversation.id
    else:
        conversation = Conversation.objects.get(id=request.session['conversation_id'])

    # Save user message
    user_input = request.POST.get("text")
    Message.objects.create(conversation=conversation, text=user_input, role='user')

    # TODO: Get chatbot's response here
    bot_response = "Hello, this is a placeholder response."

    # Save bot message
    Message.objects.create(conversation=conversation, text=bot_response, role='assistant')

    return JsonResponse({"text": bot_response})
