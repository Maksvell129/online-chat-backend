from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.constant import CHAT_NAME
from .models import Message
from .permissions import IsMessageAuthor
from .serializers import MessageSerializer


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageAuthor]

    def perform_update(self, serializer):
        # Call the parent perform_update method to update the message
        super().perform_update(serializer)

        # Send a WebSocket message to notify clients of the update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            CHAT_NAME,
            {
                'type': 'message_updated',
                'message': serializer.data,
            }
        )

    def perform_destroy(self, instance):
        # Get the message ID before it's deleted
        message_id = instance.id

        # Call the parent perform_destroy method to delete the message
        super().perform_destroy(instance)

        # Send a WebSocket message to notify clients of the deletion
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            CHAT_NAME,
            {
                'type': 'message_deleted',
                'message_id': message_id,
            }
        )
