from datetime import datetime, timedelta, timezone
from pathlib import Path


import jwt
from jwt.exceptions import InvalidTokenError

from src.providers.settings_provider import settings



def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_private_key_path.read_text(),
        algorithm=settings.algorithm,
    )

    return encoded_jwt


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
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNyIsImV4cCI6MTc3NzQwOTg4NX0.idRV8N7HLsNTTfGnIou_2Xnn-qPbDu3ws8xvo2TUfaQ"
    print(decode_access_token(token))