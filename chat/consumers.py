from json import loads, dumps
from json.decoder import JSONDecodeError

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.serializers import MessageSerializer
from chat.services import MessageService
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user: User = self.scope['user']
        self.room_group_name = "chat"

        await self.accept()
        if self.user.is_anonymous:
            await self.close(code=4003)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_join",
                "username": self.user.username,
            },
        )

        messages = await database_sync_to_async(MessageService.get_all_messages_serialized)()

        await self.send(text_data=dumps(
            {
                "type": "message_history",
                "messages": messages,
            })
        )

    async def disconnect(self, close_code):
        # Leave room group

        # send the leave event to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_leave",
                "username": self.user.username,
            },
        )
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = loads(text_data)
            message = text_data_json["message"]
        except JSONDecodeError:
            message = text_data

        message = await database_sync_to_async(MessageService.save_message)(message, self.user)
        serialized_message = MessageSerializer(message).data

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": serialized_message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=dumps({
            "type": "chat_message",
            "message": message,
        }))

    async def user_join(self, event):
        username = event["username"]
        await self.send(text_data=dumps({
            "type": "user_join",
            "username": username
        }))

    async def user_leave(self, event):
        username = event["username"]
        await self.send(text_data=dumps({
            "type": "user_leave",
            "username": username
        }))
