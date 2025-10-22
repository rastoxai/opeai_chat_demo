# app.py
from fastapi import FastAPI
import requests
import os

app = FastAPI(title="MCP Demo (Local)")

# Set default MCP endpoint
MCP_BASE = os.environ.get("MCP_BASE", "http://localhost:5011")
MCP_METADATA_PATH = os.environ.get("MCP_METADATA_PATH", "/api/metadata")

@app.get("/hello")
def hello():
    return {"message": "Hello World from  AgentKit Demo (Local)"}

@app.get("/mcp/metadata")
def get_mcp_metadata():
    """Fetch metadata from local MCP (mock or real)."""
    url = MCP_BASE.rstrip("/") + MCP_METADATA_PATH
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {"status": "success", "metadata": data}
    except Exception as e:
        return {"status": "error", "details": str(e)}
    
from fastapi.staticfiles import StaticFiles
import pathlib

app.mount("/.well-known", StaticFiles(directory=pathlib.Path(__file__).parent / ".well-known"), name="static")

