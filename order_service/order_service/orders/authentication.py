from rest_framework import authentication, exceptions
from django.conf import settings
import jwt

class StatelessJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication for both service accounts and user accounts.
    """
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        token = auth_header[1].decode('utf-8')

        try:
            # Decode the token with the signing key
            decoded = jwt.decode(
                token,
                settings.SIMPLE_JWT['SIGNING_KEY'],
                algorithms=[settings.SIMPLE_JWT['ALGORITHM']],
                options={'verify_aud': False},  # Adjust as needed
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        # Separate logic for service accounts
        if 'service_name' in decoded:
            # Token is from a service account
            return (ServiceAccount(decoded), token)
        else:
            # Token is from a regular user
            return (SimpleUser(decoded), token)

class SimpleUser:
    def __init__(self, token_payload):
        self.token = token_payload
        self.id = token_payload.get('user_id')
        self.role = token_payload.get('role')
        self.permissions = token_payload.get('permissions', [])

    def is_authenticated(self):
        return True

class ServiceAccount:
    def __init__(self, token_payload):
        self.token = token_payload
        self.service_name = token_payload.get('service_name')
        self.permissions = token_payload.get('permissions', [])

    def is_authenticated(self):
        return True