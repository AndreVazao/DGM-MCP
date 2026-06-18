import os
from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from rich.console import Console
import uvicorn

from ..core.runtime import MCPRuntime
from ..config.config_manager import ConfigManager

console = Console()

app = FastAPI(title="DGM-MCP Web")

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
    # Aqui ligar ao runtime real no futuro
    return {"status": "received", "description": description}

def start_web():
    console.print("[green]🌐 Interface Web iniciada em http://127.0.0.1:8001[/green]")
    uvicorn.run(app, host="127.0.0.1", port=8001)
