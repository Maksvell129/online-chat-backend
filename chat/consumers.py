from json import loads, dumps
from json.decoder import JSONDecodeError

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from chat.services import MessageService
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user: User = self.scope['user']
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.accept()
        if not self.user.is_anonymous:
            # Join room group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        else:
            await self.close(code=4003)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = loads(text_data)
            message = text_data_json["message"]
        except JSONDecodeError:
            message = text_data

        await database_sync_to_async(MessageService.save_message)(message, self.user)

        await database_sync_to_async(MessageService.save_message)(message, self.scope['user'])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=dumps({"message": message, 'sender': self.user.username}))
