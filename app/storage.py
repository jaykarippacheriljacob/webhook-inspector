"""
In-memory storage for captured requests, plus the idempotency cache.

There is no database on purpose: an inspector wants a fresh slate on restart.
A deque with maxlen is a ring buffer — once it is full, adding a new item
drops the oldest automatically, so memory can never grow without bound.
"""
from collections import deque

from app.config import MAX_STORED

# Newest request first. maxlen makes it self-trimming.
requests_log: deque = deque(maxlen=MAX_STORED)

# Idempotency-Key -> the record we returned the first time we saw that key.
idempotency_cache: dict = {}


def add(record: dict) -> None:
    requests_log.appendleft(record)


def all_records(limit: int = 50) -> list:
    return list(requests_log)[:limit]


def find(req_id: str):
    for record in requests_log:
        if record["id"] == req_id:
            return record
    return None


def remove(req_id: str) -> bool:
    record = find(req_id)
    if record is None:
        return False
    requests_log.remove(record)
    return True


def count() -> int:
    return len(requests_log)