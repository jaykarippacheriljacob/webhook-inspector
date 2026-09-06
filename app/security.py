"""
Bearer-token authentication.

One helper, used by any route that wants protecting. It encodes the
difference interviewers love to test:
  - no / malformed credentials  -> 401 Unauthorized  ("who are you?")
  - credentials that don't match -> 403 Forbidden     ("you can't do this")
If `expected` is None the check is skipped, so auth is opt-in per deployment.
"""
from typing import Optional

from fastapi import HTTPException


def require_token(authorization: Optional[str], expected: Optional[str]) -> None:
    if not expected:                       # auth disabled for this token
        return
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header.")
    if authorization.removeprefix("Bearer ").strip() != expected:
        raise HTTPException(status_code=403, detail="Token not accepted for this resource.")