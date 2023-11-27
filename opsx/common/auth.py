import jwt
from django.db.models import Q
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model


def get_authorization_header(request):
    """
    Return request's 'Authorization:' header, as a bytestring.

    Hide some test client ickyness where the header can be unicode.
    """
    token = request.META.get('HTTP_AUTHORIZATION', b'')
    # sign = request.META.get('HTTP_SIGN', b'')
    # if sign:
    #     auth = {
    #         'type': 'api',
    #         'token': sign,
    #         'username': request.META.get('HTTP_USERNAME', b''),
    #         'password': request.META.get('HTTP_PASSWORD', b''),
    #     }
    # else:
    auth = {'type': 'token', 'token': token}
    if isinstance(token, str):
        auth['token'] = auth['token'].encode(HTTP_HEADER_ENCODING)
    return auth


class GlobalTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request)
        if not auth:
            raise exceptions.NotAuthenticated(_("Token has expired"))
        try:
            token = auth['token']
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        if auth['type'] == 'token':
            return self.authenticate_credentials(token)

    def authenticate_credentials(self, access_token):
        username = self.decode_token(access_token)
        if not username:
            raise exceptions.AuthenticationFailed(_('Token decodes fail'))
        user_obj = get_user_model()
        user = user_obj.objects.filter(Q(username=username) | Q(first_name=username)).first()
        if not user:
            raise exceptions.AuthenticationFailed(_("User does not exist"))
        if not user.is_active:
            raise exceptions.AuthenticationFailed(_("User is not active"))
        return user, 'token'

    def decode_token(self, token):
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            return decode_token['username']
        except jwt.ExpiredSignatureError:
            # print("Token expired")
            return None
        except jwt.InvalidTokenError:
            # print("Invalid Token")
            return None
