from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView
from rest_framework import routers

from . import views

app_name = "flashcards"


router = routers.DefaultRouter()
router.register("conversation", views.ConversationViewSet, basename="conversation")


# ToDo: Consider how these change with django-ninja or drf
urlpatterns = [
    path("", views.chat_interface, name="chat_interface"),
    path("api/", include(router.urls)),
    path("api/whoami/", views.whoami, name="whoami"),
    path("api/csrfToken/", views.fetch_csrf, name="fetch_csrf"),
    path("api/check-csrfToken/", views.check_csrf, name="fetch_csrf"),
    path("api/auth/getToken/", views.LoginView.as_view(), name="knox_login"),
    path("api/auth/", include("knox.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", RedirectView.as_view(url="/", permanent=False), name="account_redirect"),
    path("__reload__/", include("django_browser_reload.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
