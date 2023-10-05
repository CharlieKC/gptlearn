"""
URL configuration for flashcards project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from . import views

app_name = "flashcards"

# ToDo: Consider how these change with django-ninja or drf
urlpatterns = [
    path("", views.chat_interface, name="chat_interface"),
    path("api/conversations", views.list_user_conversations, name="conversation_list_user"),
    path("api/chat/", views.api_chat, name="api_chat"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", RedirectView.as_view(url="/", permanent=False), name="account_redirect"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("chat/", views.chat_room, name="chat"),
    path("chat/<str:room_name>/", views.room, name="room"),
]
