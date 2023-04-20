from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Message(models.Model):
    """
    A model that represents a message.
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages")
    is_modified = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns a string representation of the Message instance.
        """
        return f"{self.author.username} at {self.created_at}"
