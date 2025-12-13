import base64
import hashlib
import hmac
import secrets
import time
from django.conf import settings


def generate_qr_id(pk: int, rut: str, length: int = 50, deterministic: bool = False) -> str:
    """Generate a deterministic-looking but non-reversible token based on pk and rut.

    The function uses HMAC-SHA256 with a secret (Django settings SECRET_KEY) and
    some randomness to build a URL-safe base64 string and returns exactly `length`
    characters. This is suitable for use as a QR identifier.

    Note: The generated token is non-reversible (one-way). If you need to map
    token -> id/rut, store the mapping in the DB when creating the token.
    """
    if not rut:
        rut = ""
    secret = getattr(settings, "SECRET_KEY", "super-secret-placeholder")
    if deterministic:
        # Deterministic token for a given (pk, rut) — same result for same inputs
        msg = f"{pk}:{rut}".encode()
        digest = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
        token_bytes = digest
    else:
        # timestamp and nonce add uniqueness across invocations
        ts = str(int(time.time()))
        nonce = secrets.token_bytes(8)
        # message constructed from primary inputs
        msg = f"{pk}:{rut}:{ts}:{nonce.hex()}".encode()
        digest = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
        # combine digest + nonce for more entropy
        token_bytes = digest + nonce
    token = base64.urlsafe_b64encode(token_bytes).decode().rstrip("=")
    # ensure length; truncate or pad as needed
    if len(token) >= length:
        return token[:length]
    # pad with additional secure random base64
    while len(token) < length:
        token += base64.urlsafe_b64encode(secrets.token_bytes(4)).decode().rstrip("=")
    return token[:length]
