from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from flashcards.serializers import ConversationSerializer

from .models import Conversation


@login_required(login_url="/accounts/login/")
def chat_interface(request):
    return render(request, "chat_interface.html")


@login_required(login_url="/accounts/login/")
def list_user_conversations(request):
    """This endpoint will list the user conversations"""
    conversations = list(Conversation.objects.filter(user=request.user).all())
    data = serialize("json", conversations)
    return JsonResponse(data, safe=False)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    pagination_class.page_size_query_param = "page_size"
    pagination_class.max_page_size = 50

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(user=user).order_by("-created_at")
        else:
            return Conversation.objects.none()


def chat_room(request):
    return render(request, "chat/index.html")


def room(request, room_name: str):
    return render(request, "chat/room.html", {"room_name": room_name})
