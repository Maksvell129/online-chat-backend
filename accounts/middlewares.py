from .services import get_user
from django.contrib.auth.models import AnonymousUser
from channels.db import close_old_connections
from urllib.parse import parse_qs


class QueryParamsMiddleware:
    """
    A middleware that extracts query parameters from the request and adds them to the scope.
    """

    async def __call__(self, scope, receive, send):
        """
        Extracts the query string from the scope, decodes it, and parses it into a dictionary of key-value pairs.
        The resulting dictionary is added to the scope with the key 'query_params'.
        """
        scope['query_params'] = parse_qs(scope['query_string'].decode())
        return await self.inner(scope, receive, send)


class JWTAuthMiddleware:
    """
    A middleware that authenticates requests using JWT access tokens.
    """

    async def __call__(self, scope, receive, send):
        """
        Authenticates the request using a JWT access token. If a valid access token is found, the associated user
        is retrieved from the database and added to the scope with the key 'user'. If no valid access token is found,
        an anonymous user is created and added to the scope.
        """
        close_old_connections()

        try:
            access_token = scope['query_params']['access_token'][-1]
            user = await get_user(access_token)
        except KeyError:
            user = AnonymousUser()
        scope['user'] = user

        return await self.inner(scope, receive, send)
