import time
from collections import defaultdict
from fastapi import Request, HTTPException, status


class SimpleRateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.ip_history = defaultdict(list)

    def check_rate_limit(self, request: Request):
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        window_start = now - 60.0

        # Filter out requests older than 1 minute
        history = [t for t in self.ip_history[client_ip] if t > window_start]
        history.append(now)
        self.ip_history[client_ip] = history

        if len(history) > self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please wait a minute before sending more requests."
            )


limiter = SimpleRateLimiter(requests_per_minute=60)


def rate_limit(request: Request):
    limiter.check_rate_limit(request)
