from django.urls import path
from . import views

urlpatterns = [
    path("message/", views.chat_message_view, name="chat_message"),
    path("messages/", views.chat_messages_view, name="chat_messages"),
    path("del_messages/", views.delete_all_messages, name="del_chat_messages"),
]
