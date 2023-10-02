import string
from django.shortcuts import render
from django.http import JsonResponse
from .models import Conversation, Message
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize


@login_required(login_url='/accounts/login/')
def chat_interface(request):
    messages = []

    if request.user.is_authenticated:
        if conversation_id := request.session.get('conversation_id'):
            conversation = Conversation.objects.get(user=request.user, id=conversation_id)
        else:
            conversation = Conversation.objects.create(user=request.user)
            conversation.save()
            request.session['conversation_id'] = conversation.id
            

        for msg in conversation.messages.all():
            messages.append(msg)
    return render(request, 'chat_interface.html', {"messages": messages})

@login_required(login_url='/accounts/login/')
def list_user_conversations(request):
    """This endpoint will list the user conversations"""
    conversations = Conversation.objects.filter(user=request.user).all()
    return JsonResponse(serialize('json', conversations), safe=False)

markdowntext = '''
# this is some code

here

``` python
print("hello world")
```

```python
# this is a comment
print("hello world!")
```

:::python
print('hellow world')


Here are my projects `models.py`

``` python
# {(Path(__file__).parent / "models.py").read_text()}
```

# How about an image?

![Tux, the Linux mascot]({% static images/cat.png %})


'''

def conversation_list(request):
    """Show a list of all the conversations!"""
    return render(request, 'conversation_list.html', {"markdowntext": markdowntext})

def api_chat(request):
    # Create a new conversation if one doesn't exist
    if 'conversation_id' not in request.session:
        conversation = Conversation.objects.create(user=request.user)
        request.session['conversation_id'] = conversation.id
    else:
        conversation = Conversation.objects.get(user=request.user, id=request.session['conversation_id'])

    # Save user message
    user_input = request.POST.get("text")
    Message.objects.create(conversation=conversation, text=user_input, role='user')

    # TODO: Get chatbot's response here
    bot_response = "Hello, this is a placeholder response."

    # Save bot message
    Message.objects.create(conversation=conversation, text=bot_response, role='assistant')

    return JsonResponse({"text": bot_response})
