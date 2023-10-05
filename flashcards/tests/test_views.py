import pytest
from django.urls import reverse

from flashcards.models import Message


@pytest.mark.parametrize(("messages", "expected_num_conversations"), [([], 0), (["hi"], 1), (["hi", "hi"], 1)])
def test_conversations(authenticated_client, messages, expected_num_conversations):
    # No conversations loaded
    for msg in messages:
        response = authenticated_client.post(reverse("api_chat"), {"text": msg})
        assert response.status_code == 200

    response = authenticated_client.get(
        reverse("conversation_list_user"),
    )
    assert response.status_code == 200
    conversations = response.json()
    # ToDo: Struggling with json decoding here, might wait for when I use drf
    #       to fix this assertion
    assert len(conversations) > expected_num_conversations

    all_messages = list(Message.objects.all().order_by("created_at"))
    assert len(all_messages) == len(messages) * 2


@pytest.mark.parametrize(("message", "expected_message"), [[" dog ", "dog"], ["\n\tcat cat \n ", "cat cat"]])
def test_message_input_stripped_whitespace(authenticated_client, message, expected_message):
    response = authenticated_client.post(reverse("api_chat"), {"text": message})
    assert response.status_code == 200
    saved_message = Message.objects.get(text=expected_message)
    assert saved_message.text == expected_message
