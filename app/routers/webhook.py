"""
The /webhook receiver — the endpoint you point real webhooks at.

It accepts any common method, then runs three gates in order before storing:
  1. rate limit   -> 429
  2. auth         -> 401 / 403
  3. idempotency  -> replay the first result instead of duplicating
and finally returns 201 Created with an echo of what it captured.
"""
from typing import Optional

from fastapi import APIRouter, Request, Header
from fastapi.responses import JSONResponse

from app import config, storage
from app.capture import capture, client_ip
from app.rate_limit import is_rate_limited
from app.security import require_token

router = APIRouter()


@router.api_route("/webhook", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def receive_webhook(
    request: Request,
    authorization: Optional[str] = Header(default=None),
    idempotency_key: Optional[str] = Header(default=None),
):
    # 1) rate limiting
    if is_rate_limited(client_ip(request)):
        return JSONResponse(
            status_code=429,
            content={"error": "rate_limited",
                     "detail": f"Limit is {config.RATE_LIMIT} requests per minute."},
            headers={"Retry-After": "60"},
        )

    # 2) authentication (only if API_TOKEN is configured)
    require_token(authorization, config.API_TOKEN)

    # 3) idempotency: a repeated key returns the first result, never a duplicate
    if idempotency_key and idempotency_key in storage.idempotency_cache:
        prior = storage.idempotency_cache[idempotency_key]
        return JSONResponse(status_code=200, content={"idempotent_replay": True, **prior})

    record = await capture(request)
    storage.add(record)
    if idempotency_key:
        storage.idempotency_cache[idempotency_key] = record

    return JSONResponse(status_code=201, content={"captured": True, **record})