from django.contrib import admin
from chat_app.models import ChatMessage


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "text", "created_at")


admin.site.register(ChatMessage, ChatMessageAdmin)
