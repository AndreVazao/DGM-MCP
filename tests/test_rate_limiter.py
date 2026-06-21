import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dgm_mcp.web.rate_limiter import RateLimitMiddleware
import time

def test_rate_limiter_throttling():
    app = FastAPI()
    # 2 requests per second, 5 per minute
    app.add_middleware(RateLimitMiddleware, req_per_second=2, req_per_minute=5)

    @app.get("/")
    async def root():
        return {"message": "ok"}

    client = TestClient(app)

    # First two requests should pass
    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 200

    # Third request in the same second should fail
    resp = client.get("/")
    assert resp.status_code == 429
    assert resp.json()["detail"] == "Too Many Requests"

def test_rate_limiter_minute_burst():
    app = FastAPI()
    # High per second, low per minute
    app.add_middleware(RateLimitMiddleware, req_per_second=100, req_per_minute=3)

    @app.get("/")
    async def root():
        return {"message": "ok"}

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 200

    # 4th request should fail minute limit
    assert client.get("/").status_code == 429

def test_rate_limiter_recovery():
    app = FastAPI()
    app.add_middleware(RateLimitMiddleware, req_per_second=1, req_per_minute=10)

    @app.get("/")
    async def root():
        return {"message": "ok"}

    client = TestClient(app)

    assert client.get("/").status_code == 200
    assert client.get("/").status_code == 429

    # Wait for recovery
    time.sleep(1.1)
    assert client.get("/").status_code == 200
