"""
A tiny in-memory sliding-window rate limiter.

For each IP we keep the timestamps of its recent hits. On each call we drop
timestamps older than 60 seconds; if what remains is already at the limit,
the caller is limited. Simple, no dependencies — good enough for a demo and
enough to talk about the idea in an interview.
"""
import time
from collections import defaultdict

from app.config import RATE_LIMIT

_buckets: dict = defaultdict(list)  # ip -> [timestamps within the last minute]


def is_rate_limited(ip: str) -> bool:
    now = time.time()
    recent = [t for t in _buckets[ip] if now - t < 60]
    _buckets[ip] = recent
    if len(recent) >= RATE_LIMIT:
        return True
    recent.append(now)
    return False 