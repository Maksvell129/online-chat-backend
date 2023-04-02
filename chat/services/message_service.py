from typing import List, Dict

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from chat.models import Message
from chat.serializers import MessageSerializer

User = get_user_model()


class MessageService:

    @staticmethod
    def save_message(message: str, user: User) -> Message:
        """
        Create message with given parameters
        """
        return Message.objects.create(
            author=user,
            content=message,
        )

    @staticmethod
    def get_all_messages() -> QuerySet[Message]:
        return Message.objects.all()

    @staticmethod
    def get_all_messages_serialized() -> List[Dict]:
        messages = MessageService.get_all_messages()
        return MessageSerializer(messages, many=True).data
