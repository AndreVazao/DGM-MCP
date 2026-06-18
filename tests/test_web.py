import pytest
import os
from fastapi.testclient import TestClient
from dgm_mcp.web.app import app

client = TestClient(app)

def test_web_no_api_key_env():
    # If DGM_API_KEY is not set, it should allow access
    with pytest.MonkeyPatch().context() as m:
        m.delenv("DGM_API_KEY", raising=False)
        # We need to reload the module or the variable API_KEY in app.py
        import importlib
        import dgm_mcp.web.app
        importlib.reload(dgm_mcp.web.app)

        from dgm_mcp.web.app import app as reloaded_app
        reloaded_client = TestClient(reloaded_app)
        response = reloaded_client.get("/")
        assert response.status_code == 200

def test_web_with_api_key_unauthorized():
    os.environ["DGM_API_KEY"] = "secret"
    import importlib
    import dgm_mcp.web.app
    importlib.reload(dgm_mcp.web.app)

    from dgm_mcp.web.app import app as reloaded_app
    reloaded_client = TestClient(reloaded_app)

    response = reloaded_client.get("/")
    assert response.status_code == 401
    assert response.json()["detail"] == "API key inválida"

def test_web_with_api_key_authorized():
    os.environ["DGM_API_KEY"] = "secret"
    import importlib
    import dgm_mcp.web.app
    importlib.reload(dgm_mcp.web.app)

    from dgm_mcp.web.app import app as reloaded_app
    reloaded_client = TestClient(reloaded_app)

    response = reloaded_client.get("/", headers={"X-DGM-KEY": "secret"})
    assert response.status_code == 200
