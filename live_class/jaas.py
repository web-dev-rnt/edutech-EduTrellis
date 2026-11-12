"""JaaS (Jitsi as a Service by 8x8): classes embedded in the site, with admins as hosts automatically.

Each person who opens a class gets a short-lived token signed with the JaaS private key. Staff tokens say
"moderator", so admins never see Jitsi's "log in to become a moderator" screen; students join as participants.
Set JAAS_APP_ID, JAAS_API_KEY_ID and JAAS_PRIVATE_KEY (see .env.example) to switch it on.
"""
import base64
import json
import time

from django.conf import settings

DOMAIN = '8x8.vc'
TOKEN_SECONDS = 4 * 60 * 60


def is_configured():
    return bool(settings.JAAS_APP_ID and settings.JAAS_API_KEY_ID and settings.JAAS_PRIVATE_KEY)


def room(room_name):
    return f"{settings.JAAS_APP_ID}/{room_name}"


def script_url():
    return f"https://{DOMAIN}/{settings.JAAS_APP_ID}/external_api.js"


def _b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def _private_key():
    from cryptography.hazmat.primitives import serialization
    pem = settings.JAAS_PRIVATE_KEY.replace('\\n', '\n').strip()  # one-line form from environment variables
    return serialization.load_pem_private_key(pem.encode(), password=None)


def token(user, display_name, moderator):
    """RS256 JWT in the format JaaS expects (string "true"/"false" flags, as in the 8x8 docs)."""
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    now = int(time.time())
    flag = lambda value: 'true' if value else 'false'
    header = {'alg': 'RS256', 'kid': settings.JAAS_API_KEY_ID, 'typ': 'JWT'}
    payload = {
        'aud': 'jitsi', 'iss': 'chat', 'sub': settings.JAAS_APP_ID, 'room': '*',
        'iat': now, 'nbf': now - 10, 'exp': now + TOKEN_SECONDS,
        'context': {
            'user': {
                'id': str(user.pk), 'name': display_name, 'email': user.email or '', 'avatar': '',
                'moderator': flag(moderator), 'hidden-from-recorder': 'false',
            },
            'features': {
                'livestreaming': 'false', 'recording': 'false', 'transcription': 'false',
                'outbound-call': 'false', 'sip-outbound-call': 'false',
            },
        },
    }
    signing_input = '.'.join(_b64(json.dumps(part, separators=(',', ':')).encode()) for part in (header, payload))
    signature = _private_key().sign(signing_input.encode(), padding.PKCS1v15(), hashes.SHA256())
    return f"{signing_input}.{_b64(signature)}"
