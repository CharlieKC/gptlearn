from django.contrib import admin

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0  # Number of empty forms to display
    readonly_fields = ["created_at"]  # Fields to display as read-only


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    list_display = ["id", "user", "created_at", "updated_at"]
    readonly_fields = ["user", "created_at", "updated_at"]


admin.site.register(Message)
