from starlette.middleware.authentication import (
    AuthCredentials, AuthenticationError
)
from starlette.authentication import AuthenticationBackend
from services import check_user_token


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        method = request.scope.get('method')
        path = request.scope.get('path')

        if method == 'POST' and path in ['/', '/token', '/user']:
            return

        if "Authorization" not in request.headers:
            raise AuthenticationError('Invalid token.')

        auth = request.headers["Authorization"]
        try:
            token = auth.split('Token')[1].strip()
        except IndexError:
            raise AuthenticationError('Invalid token.')

        user = check_user_token(token)
        user.is_authenticated = True

        return AuthCredentials(["authenticated"]), user
