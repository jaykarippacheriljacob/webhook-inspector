"""
Turn an incoming Request into a plain dict we can store and return as JSON.

This is the heart of the "inspector": it reads the method, path, query,
headers and body, and stamps each capture with an id and a timestamp. The
Authorization header is masked so a real secret is never stored or echoed.
"""
import uuid
from datetime import datetime, timezone

from fastapi import Request


def client_ip(request: Request) -> str:
    """Real client IP, honouring a proxy's X-Forwarded-For if present."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


async def capture(request: Request) -> dict:
    raw = await request.body()
    try:
        body = raw.decode("utf-8")
    except UnicodeDecodeError:
        body = f"<{len(raw)} bytes of binary data>"

    headers = dict(request.headers)
    if "authorization" in headers:                      # never echo a full secret
        headers["authorization"] = headers["authorization"][:12] + "…(masked)"

    return {
        "id": uuid.uuid4().hex[:8],
        "received_at": datetime.now(timezone.utc).isoformat(),
        "method": request.method,
        "path": request.url.path,
        "query": dict(request.query_params),
        "headers": headers,
        "body": body,
        "client_ip": client_ip(request),
    }