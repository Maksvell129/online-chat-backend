from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser


@database_sync_to_async
def get_user(auth_header):
    auth = JWTAuthentication()
    try:
        validated_token = auth.get_validated_token(auth_header)
    except InvalidToken:
        return AnonymousUser()

    user_id = validated_token['user_id']
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
