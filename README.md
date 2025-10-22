
## MCP Demo App

**A demo FastAPI app showcasing how an internal MCP (Model Context Protocol) service can be exposed and integrated as a ChatGPT App / AgentKit connector.**

This app serves as a **local demo**, with optional deployment to **Cloud Run** for public access and integration with ChatGPT Apps (App Store / Plugins). It demonstrates:

- Fetching metadata from a local MCP instance.
- Serving a “Hello World” endpoint.
- Exposing `.well-known/ai-plugin.json` manifest and OpenAPI schema for ChatGPT discovery.
- Acting as a blueprint for internal AgentKit-style connectors.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Setup and Installation](#setup-and-installation)
4. [Running the App Locally](#running-the-app-locally)
5. [Testing Endpoints](#testing-endpoints)
6. [Demo with Mock MCP](#demo-with-mock-mcp)
7. [Exposing App to ChatGPT Apps](#exposing-app-to-chatgpt-apps)
8. [Deployment to Cloud Run](#deployment-to-cloud-run)
9. [Security & Access Control](#security--access-control)
10. [Next Steps](#next-steps)

---

## Prerequisites

- Python 3.11+
- `pip` or virtual environment support
- Optional: [ngrok](https://ngrok.com/) for public endpoint demo
- Optional: Google Cloud SDK for Cloud Run deployment
- Optional: running MCP instance (or mock MCP included)

---

## Project Structure

```

app\_demo/
├─ app.py \# Main FastAPI app
├─ requirements.txt \# Python dependencies
├─ .well-known/
│ ├─ ai-plugin.json \# ChatGPT plugin manifest
│ └─ openapi.yaml \# OpenAPI schema
├─ mock\_mcp.py \# Optional mock MCP server

````

---

## Setup and Installation

1. Clone or download this repository.
2. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
````

3.  Install dependencies:

<!-- end list -->

```bash
pip install -r requirements.txt
```

4.  (Optional) Configure environment variables if MCP runs on a custom host/port:

<!-- end list -->

```bash
export MCP_BASE="http://localhost:5000"
export MCP_METADATA_PATH="/api/metadata"
```

-----

## Running the App Locally

Run the application using `uvicorn`:

```bash
uvicorn app:app --reload --port 8080
```

  - Visit `http://localhost:8080/hello`
    → “Hello World” message
  - Visit `http://localhost:8080/mcp/metadata`
    → Fetches metadata from MCP

-----

## Testing Endpoints

Use a browser, Postman, or CLI to verify the endpoints.

```bash
curl http://localhost:8080/hello
curl http://localhost:8080/mcp/metadata
```

Verify `.well-known` files:

```
http://localhost:8080/.well-known/ai-plugin.json
http://localhost:8080/.well-known/openapi.yaml
```

-----

## Demo with Mock MCP

If an actual MCP is not running locally, use `mock_mcp.py` to provide sample data:

```bash
uvicorn mock_mcp:app --port 5000
```

This provides sample metadata JSON to test the demo app.

-----

## Exposing App to ChatGPT Apps

1.  Install and run `ngrok` (for temporary public HTTPS):

<!-- end list -->

```bash
ngrok http 8080
```

2.  **Update** `.well-known/ai-plugin.json` with the ngrok URL:

<!-- end list -->

```json
"api": {
  "type": "openapi",
  "url": "https://<ngrok-id>.ngrok.io/.well-known/openapi.yaml",
  "is_user_authenticated": false
}
```

3.  **Register** the manifest in ChatGPT (Plus/Enterprise account):

      - Navigate to **Explore GPTs** → **Build a GPT** or **Plugins** → **Develop your own**
      - Enter the manifest URL (`.well-known/ai-plugin.json`)
      - ChatGPT fetches the OpenAPI schema and installs the app

4.  **Test** by asking ChatGPT:

> Get MCP metadata

-----

## Deployment to Cloud Run

Ensure a `Dockerfile` exists (or use `--source .` deployment).

Deploy:

```bash
gcloud run deploy mcp-demo \
  --source . \
  --platform managed \
  --region australia-southeast1 \
  --allow-unauthenticated
```

Update `.well-known/ai-plugin.json` to use the Cloud Run HTTPS URL.

-----

## Security & Access Control

  - **Demo mode** (`auth.type: "none"`) is accessible to anyone with the manifest URL (safe for short demo only).
  - **Internal / Production**: use `service_http` or `user_http` authentication to restrict access.
  - Cloud Run supports **IP allowlisting** or **VPC restrictions** for enterprise deployments.

-----

## Next Steps

  - Replace mock MCP with a real MCP backend.
  - Integrate with AgentKit workflows for internal agents.
  - Add authentication (`service_http` / OAuth) for secure usage.
  - Extend endpoints for other internal/enxternal systems (CMS, CRM, AdOps).
  - Deploy to Cloud Run and register in ChatGPT Apps for a full enterprise demo.

-----
