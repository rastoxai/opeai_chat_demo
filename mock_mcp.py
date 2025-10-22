# mock_mcp.py
from fastapi import FastAPI

app = FastAPI(title="Mock MCP Server")

@app.get("/api/metadata")
def metadata():
    return {
        "instance": "mock-mcp",
        "version": "0.1.0",
        "connected_tools": [
            {"name": "content-analyzer", "type": "model", "status": "ready"},
            {"name": "asset-indexer", "type": "pipeline", "status": "ok"}
        ],
        "schemas": {
            "article": {"fields": ["id", "title", "author", "created_at"]},
            "media_asset": {"fields": ["id", "url", "type"]}
        }
    }
