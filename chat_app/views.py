import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from firebase_admin import db
from chat_app.models import ChatMessage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from chat_app.serializers.chat import ChatSerializer
from rest_framework.response import Response
from datetime import datetime


@csrf_exempt
@permission_classes([IsAuthenticated])
def chat_message_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = ChatMessage(user_id=request.user.id, text=data["text"])
        message.save()
        message_data = message.as_dict()
        message_data.pop("user")
        message_data.update(
            user_id=request.user.id, created_at=datetime.now().isoformat()
        )
        print(message_data)
        db.reference("/chat_messages").push(message_data)
        return HttpResponse(json.dumps(message_data))
    else:
        return HttpResponse("Method not allowed", status=405)


@csrf_exempt
@permission_classes([IsAuthenticated])
def chat_messages_view(request):
    user_id = request.user.id
    query = db.reference("/chat_messages").order_by_child("user_id").equal_to(user_id)
    messages = query.get()
    print(messages.values())
    message_list = [ChatMessage(**msg).as_dict() for msg in messages.values()]
    message_list.sort(key=lambda x: x["created_at"])
    return HttpResponse(json.dumps(message_list))

    # query = db.reference("/chat_messages")
    # print(list(messages.values())[0].pop("user"), "---------")


@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_all_messages(request):
    # Get a reference to the chat_messages node
    chat_messages_ref = db.reference("/chat_messages")

    # Delete all messages
    chat_messages_ref.delete()

    return HttpResponse("All messages deleted successfully.")
