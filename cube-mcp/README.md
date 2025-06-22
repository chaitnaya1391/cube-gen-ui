# CubeJS MCP Server

This is a Model Context Protocol (MCP) server that provides access to CubeJS API endpoints via SSE (Server-Sent Events) transport.

## Overview

The MCP server exposes two main tools:
- `cubejs_meta`: Get metadata about available cubes, dimensions, and measures
- `cubejs_load`: Execute CubeJS queries to load data

## Configuration

The server requires the following environment variables:
- `CUBEJS_BASE_URL`: The base URL of your CubeJS instance (required)
- `CUBEJS_API_TOKEN`: API token for authentication (optional)
- `MCP_PORT`: Port for the SSE server (default: 8000)

## Usage

### Running with Docker

The MCP server runs as an HTTP service using SSE transport.

To run the MCP server:
```bash
# Build the MCP container
make mcp-build

# Run the MCP server (starts HTTP server on port 8000)
make mcp-run
```

Or using Docker Compose directly:
```bash
# Build the container
docker compose build mcp

# Run the container
docker compose up mcp
```

The server will be available at `http://localhost:8000` with SSE endpoint at `/messages`.

### Running Locally

```bash
# Install dependencies
pip install -e .

# Set environment variables
export CUBEJS_BASE_URL=http://localhost:4000
export CUBEJS_API_TOKEN=your-token-here
export MCP_PORT=8000

# Run the server
python main.py
```

## MCP Client Integration

This server is designed to work with MCP clients like Claude Desktop or other MCP-compatible applications. The server communicates via SSE (Server-Sent Events) over HTTP using the MCP protocol.

To connect to this server from an MCP client, use:
- URL: `http://localhost:8000/messages`
- Transport: SSE

## Available Tools

### cubejs_meta
Returns metadata about available cubes, dimensions, and measures from the CubeJS instance.

### cubejs_load
Executes a CubeJS query and returns the results. Requires a `query` parameter with the CubeJS query structure.

Example query structure:
```json
{
  "measures": ["Orders.count"],
  "dimensions": ["Orders.status"],
  "timeDimensions": [
    {
      "dimension": "Orders.createdAt",
      "granularity": "month"
    }
  ]
}
```

## Architecture

The server acts as a bridge between MCP clients and the CubeJS REST API, providing a standardized interface for querying cube data through the Model Context Protocol over SSE transport.

## Dependencies

- `mcp>=1.0.0`: MCP protocol implementation
- `httpx>=0.25.0`: HTTP client for CubeJS API calls
- `uvicorn>=0.24.0`: ASGI server for SSE transport
