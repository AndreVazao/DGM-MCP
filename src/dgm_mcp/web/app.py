import os
from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from rich.console import Console
import uvicorn

from ..core.runtime import MCPRuntime
from ..config.config_manager import ConfigManager
from .rate_limiter import RateLimitMiddleware

console = Console()

app = FastAPI(title="DGM-MCP Web")
app.add_middleware(RateLimitMiddleware, req_per_second=5, req_per_minute=50)

# Global runtime instance for the web app
_runtime = None

def get_runtime():
    global _runtime
    if _runtime is None:
        config = ConfigManager().load()
        _runtime = MCPRuntime(config)
        _runtime.start()
    return _runtime

API_KEY = os.getenv("DGM_API_KEY")

def validate_api_key(x_dgm_key: str = Header(default="")):
    if not API_KEY:
        return
    if x_dgm_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API key inválida"
        )

@app.get("/", response_class=HTMLResponse)
async def home(api_key: None = Depends(validate_api_key)):
    return """
    <h1>DGM-MCP Dashboard</h1>
    <p>Interface web simples para controlar o MCP</p>
    <form action="/task" method="post">
        <textarea name="description" rows="5" cols="80" placeholder="Descreve a tarefa..."></textarea><br>
        <button type="submit">Enviar Tarefa</button>
    </form>
    """

@app.post("/task")
async def create_task(request: Request, api_key: None = Depends(validate_api_key)):
    data = await request.form()
    description = data.get("description")
    runtime = get_runtime()
    task = runtime.task_manager.create_task(description)
    return {"status": "received", "task_id": task.id}

@app.get("/health")
async def health(runtime: MCPRuntime = Depends(get_runtime)):
    return {
        "status": "ok",
        "runtime": runtime.running,
        "tools": len(runtime.tools),
        "llm_provider": runtime.llm_manager.current_provider.name.lower() if runtime.llm_manager.current_provider else "none"
    }

@app.get("/metrics")
async def metrics(runtime: MCPRuntime = Depends(get_runtime)):
    obs = runtime.observability
    return {
        "tasks_total": obs.tasks_total,
        "tasks_success": obs.tasks_success,
        "tasks_failed": obs.tasks_failed,
        "tool_calls": obs.tool_calls
    }

def start_web():
    console.print("[green]🌐 Interface Web iniciada em http://127.0.0.1:8001[/green]")
    uvicorn.run(app, host="127.0.0.1", port=8001)
