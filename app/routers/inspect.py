"""
Read and manage what /webhook captured, plus a health check.

GET routes only read (safe + idempotent); DELETE mutates and returns 204.
DELETE is treated as privileged: if ADMIN_TOKEN is set it must be presented.
"""
from typing import Optional

from fastapi import APIRouter, Header, HTTPException, Response

from app import config, storage
from app.security import require_token

router = APIRouter()


@router.get("/requests")
def list_requests(limit: int = 50):
    return {"count": storage.count(), "requests": storage.all_records(limit)}


@router.get("/requests/{req_id}")
def get_request(req_id: str):
    record = storage.find(req_id)
    if record is None:
        raise HTTPException(status_code=404, detail="No captured request with that id.")
    return record


@router.delete("/requests/{req_id}", status_code=204)
def delete_request(req_id: str, authorization: Optional[str] = Header(default=None)):
    require_token(authorization, config.ADMIN_TOKEN)
    if not storage.remove(req_id):
        raise HTTPException(status_code=404, detail="No captured request with that id.")
    return Response(status_code=204)


@router.get("/health")
def health():
    return {"status": "ok", "stored": storage.count()}