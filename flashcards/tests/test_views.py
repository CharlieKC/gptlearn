import pytest
from django.urls import reverse

from flashcards.models import Conversation, Message


@pytest.mark.parametrize(("messages", "expected_num_conversations"), [([], 0), (["hi"], 1), (["hi", "hi"], 1)])
def test_conversations(authenticated_client, messages, expected_num_conversations):
    # No conversations loaded
    for msg in messages:
        response = authenticated_client.post(reverse("api_chat"), {"text": msg})
        assert response.status_code == 200

    response = authenticated_client.get(
        reverse("conversation-list"),
    )
    assert response.status_code == 200
    conversations = response.json()
    assert len(conversations) == expected_num_conversations

    all_messages = list(Message.objects.all().order_by("created_at"))

    # Here we just assume each message gets a response
    assert len(all_messages) == len(messages) * 2


@pytest.mark.parametrize(("message", "expected_message"), [[" dog ", "dog"], ["\n\tcat cat \n ", "cat cat"]])
def test_message_input_stripped_whitespace(authenticated_client, message, expected_message):
    response = authenticated_client.post(reverse("api_chat"), {"text": message})
    assert response.status_code == 200
    saved_message = Message.objects.get(text=expected_message)
    assert saved_message.text == expected_message


@pytest.mark.django_db
def test_get_queryset_authenticated_user(authenticated_client):
    # Initially there should be no conversations
    response = authenticated_client.get(reverse("conversation-list"))

    assert response.status_code == 200
    assert len(response.data) == 0

    conversation1 = Conversation.objects.create(user=authenticated_client.user)
    conversation2 = Conversation.objects.create(user=authenticated_client.user)

    response = authenticated_client.get(reverse("conversation-list"))

    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["id"] == conversation1.id
    assert response.data[1]["id"] == conversation2.id


@pytest.mark.django_db
def test_get_queryset_unauthenticated_user(client_factory):
    client = client_factory(auth=False)
    response = client.get(reverse("conversation-list"))
    assert response.status_code == 403


@pytest.mark.django_db
def test_make_new_conversation(client_factory):
    authenticated_client = client_factory()
    response = authenticated_client.post(
        reverse("conversation-list"), {"user": authenticated_client.user.id}, format="json"
    )
    assert response.status_code == 201, f"Expected 201, got {response.status_code}, {response.data}"

    conversation_id = response.data["id"]
    assert isinstance(conversation_id, int)

    # Try getting the conversation
    response = authenticated_client.get(reverse("conversation-detail", args=[conversation_id]))
    assert response.status_code == 200, f"Expected 200, got {response.status_code}, {response.data}"
    assert response.data["id"] == conversation_id
    assert response.data["user"] == authenticated_client.user.id

    # Get a second client
    authenticated_client_2 = client_factory()

    # Try getting the conversation with the second client
    response = authenticated_client_2.get(reverse("conversation-detail", args=[conversation_id]))
    assert response.status_code == 404, f"Expected 404, got {response.status_code}, {response.data}"

    # Try deleting the conversation with the second client
    response = authenticated_client_2.delete(reverse("conversation-detail", args=[conversation_id]))
    assert response.status_code == 404, f"Expected 404, got {response.status_code}, {response.data}"

    # Delete the conversation
    response = authenticated_client.delete(reverse("conversation-detail", args=[conversation_id]))
    assert response.status_code == 204, f"Expected 204, got {response.status_code}, {response.data}"

    # Try getting the conversation again
    response = authenticated_client.get(reverse("conversation-detail", args=[conversation_id]))
    assert response.status_code == 404, f"Expected 404, got {response.status_code}, {response.data}"


@pytest.mark.django_db
def test_client_factory(client_factory):
    client = client_factory()
    assert client.user.is_authenticated

    client_2 = client_factory()
    assert client_2.user.is_authenticated

    assert client.user != client_2.user

    client_3 = client_factory(auth=False)
    assert not client_3.user.is_authenticated
