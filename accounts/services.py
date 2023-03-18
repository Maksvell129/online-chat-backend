from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser


@database_sync_to_async
def get_user(auth_header):
    auth = JWTAuthentication()
    validated_token = auth.get_validated_token(auth_header)
    user_id = validated_token['user_id']
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
