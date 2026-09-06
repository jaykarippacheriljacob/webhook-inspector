"""
Configuration for the whole app, read once from environment variables.

Keeping this in one place means no other file calls os.getenv — they import
from here. Everything is optional and has a sensible default.
"""
import os

# If set, /webhook requires  Authorization: Bearer <API_TOKEN>
API_TOKEN = os.getenv("API_TOKEN")

# If set, DELETE /requests/{id} requires  Authorization: Bearer <ADMIN_TOKEN>
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

# Max /webhook requests per minute, per client IP, before a 429
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "60"))

# How many captured requests to keep in memory (a ring buffer)
MAX_STORED = int(os.getenv("MAX_STORED", "100"))