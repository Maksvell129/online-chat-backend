from .services import get_user
from django.contrib.auth.models import AnonymousUser
from channels.db import close_old_connections
from urllib.parse import parse_qs


class QueryParamsMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        scope['query_params'] = parse_qs(scope['query_string'].decode())
        return await self.inner(scope, receive, send)


class JWTAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        try:
            access_token = scope['query_params']['access_token'][-1]
            user = await get_user(access_token)
        except KeyError:
            user = AnonymousUser()
        scope['user'] = user

        return await self.inner(scope, receive, send)
