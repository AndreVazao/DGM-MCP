import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import threading
import json

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, req_per_second: int = 5, req_per_minute: int = 50):
        super().__init__(app)
        self.req_per_second = req_per_second
        self.req_per_minute = req_per_minute
        self.history = defaultdict(list)
        self.lock = threading.Lock()

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        with self.lock:
            self.history[client_ip] = [t for t in self.history[client_ip] if now - t < 60]
            recent_requests = self.history[client_ip]

            last_second_count = sum(1 for t in recent_requests if now - t < 1)
            if last_second_count >= self.req_per_second or len(recent_requests) >= self.req_per_minute:
                return Response(
                    content=json.dumps({"detail": "Too Many Requests"}),
                    status_code=429,
                    media_type="application/json"
                )

            self.history[client_ip].append(now)

        return await call_next(request)
