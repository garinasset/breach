import os
import time
import hmac
import threading
from collections import defaultdict, deque

from fastapi import HTTPException, Request


def resolve_allowed_origins() -> list[str]:
    configured = os.getenv("LEAK_CHECK_ALLOWED_ORIGINS", "").strip()
    if configured:
        return [origin.strip() for origin in configured.split(",") if origin.strip()]
    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ]


def verify_api_key(request: Request) -> None:
    configured = [
        token.strip()
        for token in os.getenv("LEAK_CHECK_API_KEYS", "").split(",")
        if token.strip()
    ]
    if not configured:
        raise HTTPException(status_code=503, detail="Server authentication is not configured")

    presented = request.headers.get("X-API-Key", "").strip()
    auth_header = request.headers.get("Authorization", "").strip()
    if not presented and auth_header.startswith("Bearer "):
        presented = auth_header[7:].strip()

    if not presented:
        raise HTTPException(status_code=401, detail="Missing API key")

    if any(hmac.compare_digest(presented, expected) for expected in configured):
        return

    raise HTTPException(status_code=401, detail="Invalid API key")


class InMemoryRateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str) -> None:
        now = time.time()
        cutoff = now - self.window_seconds
        with self._lock:
            bucket = self._events[key]
            while bucket and bucket[0] < cutoff:
                bucket.popleft()
            if len(bucket) >= self.limit:
                raise HTTPException(status_code=429, detail="Too many requests")
            bucket.append(now)


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For", "").strip()
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


RATE_LIMIT = InMemoryRateLimiter(
    limit=int(os.getenv("LEAK_CHECK_RATE_LIMIT", "30")),
    window_seconds=int(os.getenv("LEAK_CHECK_RATE_WINDOW_SECONDS", "60")),
)
