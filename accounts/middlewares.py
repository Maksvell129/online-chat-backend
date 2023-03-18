from .services import get_user
from django.contrib.auth.models import AnonymousUser
from channels.db import close_old_connections


class JWTAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                user = get_user(headers[b'authorization'].decode())
                scope['user'] = user
            except KeyError:
                pass
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)
