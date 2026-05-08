from datetime import datetime, timedelta, timezone
import base64
import hashlib
import json
from typing import Any

import jwt
from jwt import InvalidTokenError
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

from src.providers.settings_provider import settings


credential = DefaultAzureCredential()

key_client = KeyClient(
    vault_url=settings.key_vault_url,
    credential=credential,
)

key = key_client.get_key(settings.jwt_key_name)

crypto_client = CryptographyClient(
    key=key,
    credential=credential,
)


def base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def json_base64url(data: dict[str, Any]) -> str:
    return base64url(
        json.dumps(data, separators=(",", ":")).encode("utf-8")
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode = data.copy()

    now = datetime.now(timezone.utc)

    expire = now + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )

    # JWT times should be Unix timestamps.
    to_encode.update(
        {
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
            "nbf": int(now.timestamp()),
        }
    )

    header = {
        "alg": "RS256",
        "typ": "JWT",
        "kid": key.id,
    }

    encoded_header = json_base64url(header)
    encoded_payload = json_base64url(to_encode)

    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")

    # RS256 means RSA signature over SHA-256 hash.
    digest = hashlib.sha256(signing_input).digest()

    sign_result = crypto_client.sign(
        SignatureAlgorithm.rs256,
        digest,
    )

    encoded_signature = base64url(sign_result.signature)

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


if __name__ == "__main__":
    create_access_token


def decode_access_token(token: str) -> dict | None:
    """
    Decode and validates the JWT token
    """
    try:
        payload = jwt.decode( 
            token,
            settings.jwt_public_key_path.read_text(),
            algorithms=[settings.algorithm],
        )

        return payload

    except InvalidTokenError:
        return None
    

if __name__ == "__main__":
    token = create_access_token(
    data={"sub": "123"},
    expires_delta=timedelta(minutes=15),
    )

    payload = decode_access_token(token)

    print(token)
    print(payload)
