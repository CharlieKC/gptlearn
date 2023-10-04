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


# class TestUserUpdateView:
#     """
#     TODO:
#         extracting view initialization code as class-scoped fixture
#         would be great if only pytest-django supported non-function-scoped
#         fixture db access -- this is a work-in-progress for now:
#         https://github.com/pytest-dev/pytest-django/pull/258
#     """

#     def dummy_get_response(self, request: HttpRequest):
#         return None

#     def test_get_success_url(self, user: User, rf: RequestFactory):
#         view = UserUpdateView()
#         request = rf.get("/fake-url/")
#         request.user = user

#         view.request = request
#         assert view.get_success_url() == f"/users/{user.username}/"

#     def test_get_object(self, user: User, rf: RequestFactory):
#         view = UserUpdateView()
#         request = rf.get("/fake-url/")
#         request.user = user

#         view.request = request

#         assert view.get_object() == user

#     def test_form_valid(self, user: User, rf: RequestFactory):
#         view = UserUpdateView()
#         request = rf.get("/fake-url/")

#         # Add the session/message middleware to the request
#         SessionMiddleware(self.dummy_get_response).process_request(request)
#         MessageMiddleware(self.dummy_get_response).process_request(request)
#         request.user = user

#         view.request = request

#         # Initialize the form
#         form = UserAdminChangeForm()
#         form.cleaned_data = {}
#         form.instance = user
#         view.form_valid(form)

#         messages_sent = [m.message for m in messages.get_messages(request)]
#         assert messages_sent == [_("Information successfully updated")]


# class TestUserRedirectView:
#     def test_get_redirect_url(self, user: User, rf: RequestFactory):
#         view = UserRedirectView()
#         request = rf.get("/fake-url")
#         request.user = user

#         view.request = request
#         assert view.get_redirect_url() == f"/users/{user.username}/"


# class TestUserDetailView:
#     def test_authenticated(self, user: User, rf: RequestFactory):
#         request = rf.get("/fake-url/")
#         request.user = UserFactory()
#         response = user_detail_view(request, username=user.username)

#         assert response.status_code == 200

#     def test_not_authenticated(self, user: User, rf: RequestFactory):
#         request = rf.get("/fake-url/")
#         request.user = AnonymousUser()
#         response = user_detail_view(request, username=user.username)
#         login_url = reverse(settings.LOGIN_URL)

#         assert isinstance(response, HttpResponseRedirect)
#         assert response.status_code == 302
#         assert response.url == f"{login_url}?next=/fake-url/"
