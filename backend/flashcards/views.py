import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from knox.views import LoginView as KnoxLoginView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from flashcards.serializers import ConversationSerializer

from .models import Conversation

logger = logging.getLogger(__name__)


class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]

    # add logging
    def post(self, request, format=None):
        print(request.data)
        return super().post(request, format=None)


def fetch_csrf(request):
    response = JsonResponse({"detail": "CSRF cookie set"})
    response["X-CSRFToken"] = get_token(request)
    return response


@api_view(["GET"])
def whoami(request):
    return JsonResponse({"username": request.user.username})


@csrf_protect
def check_csrf(request):
    print(request.headers)
    return JsonResponse({"detail": "CSRF cookie set"})


@login_required(login_url="/accounts/login/")
def chat_interface(request):
    return render(request, "chat_interface.html")


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

    def perform_create(self, serializer):
        logger.info(f"create had been hit!, current user: {self.request.user}")
        serializer.save(user=self.request.user)
        # return super().create(request, *args, **kwargs)
