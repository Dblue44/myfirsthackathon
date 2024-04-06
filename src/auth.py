from typing import Callable
from secrets import compare_digest

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader


def token_auth(token: str, header: str = "X-API-Key") -> Callable:
    security = APIKeyHeader(name=header)

    def authorization(credentials: str = Depends(security)) -> None:
        if not compare_digest(credentials, token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect token",
            )

    return authorization
