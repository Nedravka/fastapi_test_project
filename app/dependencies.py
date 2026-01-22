from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader, APIKeyQuery
from starlette import status
from typing import Optional

from service_config import settings


api_key_header = APIKeyHeader(
    name=settings.API_KEY_NAME,
    auto_error=False,
    description="API ключ в заголовке запроса"
)

api_key_query = APIKeyQuery(
    name=settings.API_KEY_NAME,
    auto_error=False,
    description="API ключ в параметрах запроса"
)


async def get_api_key(
        api_key_header: Optional[str] = Security(api_key_header),
        api_key_query: Optional[str] = Security(api_key_query),
) -> str:
    """
    Получение и валидация API ключа.

    Ключ может быть передан:
    1. В заголовке X-API-Key
    2. В query параметре ?api_key=

    Если ключ не передан или неверный, выбрасывается HTTPException 401.
    """
    if api_key_header and api_key_header == settings.API_KEY:
        return api_key_header
    elif api_key_query and api_key_query == settings.API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Необходимо передать верный API ключ",
            headers={"WWW-Authenticate": "ApiKey"},
        )

api_key_auth = Depends(get_api_key)

public_endpoints = [
    "/",
    "/docs",
    "/redoc",
]
