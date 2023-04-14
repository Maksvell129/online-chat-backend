from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ('id', 'content', 'created_at', 'author', 'author_username', 'is_modified')

    def get_author_username(self, obj):
        return obj.author.username
