import json
from json import dumps

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.serializers import MessageSerializer
from chat.services import MessageService
from django.contrib.auth.models import User

from src.constant import CHAT_NAME


class ChatConsumer(AsyncWebsocketConsumer):
    """
    A consumer that handles WebSocket connections for a chat room.
    """

    # Dict for storing usernames of users who are online
    users_online = dict()

    async def connect(self):
        """
        Called when a WebSocket connection is established.
        """

        self.user: User = self.scope['user']
        self.room_group_name = CHAT_NAME

        # if user is anonymous close the connection
        await self.accept()
        if self.user.is_anonymous:
            await self.close(code=4003)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.add_user_to_online_users()

        # send user_join event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_join",
                "username": self.user.username,
            },
        )

        # send online_info event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "online_info",
            },
        )

        # get all messages
        messages = await database_sync_to_async(MessageService.get_all_messages_serialized)()

        # send messages history to room
        await self.send(text_data=dumps(
            {
                "type": "message_history",
                "messages": messages,
            })
        )

    async def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed.
        """

        # send user_leave event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_leave",
                "username": self.user.username,
            },
        )

        await self.remove_user_from_online_users()

        # send online_info event
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "online_info",
            },
        )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Receive message from WebSocket
        """
        # try:
        #     text_data_json = loads(text_data)
        #     message = text_data_json["message"]
        # except JSONDecodeError:
        message = text_data

        # save message
        message = await database_sync_to_async(MessageService.save_message)(message, self.user)
        serialized_message = MessageSerializer(message).data

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": serialized_message}
        )

    async def chat_message(self, event):
        """
        Receives the event chat_message and sends it to chat room.
        """
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=dumps({
            "type": "chat_message",
            "message": message,
        }))

    async def user_join(self, event):
        """
        Receives the event user_join and sends a message about it to chat room.
        """
        username = event["username"]
        await self.send(text_data=dumps({
            "type": "user_join",
            "username": username
        }))

    async def user_leave(self, event):
        """
        Receives the event user_leave and sends a message about it to chat room.
        """
        username = event["username"]
        await self.send(text_data=dumps({
            "type": "user_leave",
            "username": username
        }))

    async def online_info(self, event):
        """
        Receives the event online_info and sends info about online users to chat room.
        """
        await self.send(text_data=dumps({
            "type": "online_info",
            "users_oline": sorted(self.users_online.keys()),
        }))

    async def message_updated(self, event):
        """
        Receives the event message_updated and sends a message about it to chat room.
        """
        message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'message_updated',
            'message': message,
        }))

    async def message_deleted(self, event):
        """
        Receives the event message_deleted and sends a message about it to chat room.
        """
        message_id = event['message_id']
        await self.send(text_data=json.dumps({
            'type': 'message_deleted',
            'message_id': message_id,
        }))

    async def add_user_to_online_users(self):
        """
        Adds the current user to the dict of online users.
        """
        users_online = ChatConsumer.users_online

        users_online[self.user.username] = users_online.setdefault(self.user.username, 0) + 1

    async def remove_user_from_online_users(self):
        """
        Removes the current user from the dict of online users.
        """
        users_online = ChatConsumer.users_online

        users_online[self.user.username] -= 1

        if not users_online.get(self.user.username):
            users_online.pop(self.user.username)
