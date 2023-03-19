from django.contrib.auth import get_user_model

from chat.models import Message

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
