#!/usr/bin/env python3
"""
MCP Server for CubeJS API (SSE Transport)
Exposes meta and load endpoints from CubeJS REST API via SSE
"""

import asyncio
import json
import logging
import sys
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import httpx
from mcp.server import Server
from mcp.server.sse import SseServerTransport
# No specific MCP types needed for handlers
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CubeJSMCPServer:
    def __init__(self, base_url: str, api_token: Optional[str] = None, port: int = 8000):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.port = port
        self.server = Server("cubejs-mcp-server")
        self._setup_handlers()

    def _setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools():
            """List available CubeJS tools."""
            logger.info("Handling list_tools request")
            return [
                {
                    "name": "cubejs_meta",
                    "description": "Get metadata about available cubes, dimensions, and measures",
                    "inputSchema": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False,
                    },
                },
                {
                    "name": "cubejs_load",
                    "description": "Execute a CubeJS query to load data",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "object",
                                "description": "CubeJS query object",
                                "properties": {
                                    "measures": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Array of measure names to include"
                                    },
                                    "dimensions": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Array of dimension names to include"
                                    },
                                    "timeDimensions": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "dimension": {"type": "string"},
                                                "granularity": {"type": "string"},
                                                "dateRange": {
                                                    "oneOf": [
                                                        {"type": "string"},
                                                        {
                                                            "type": "array",
                                                            "items": {"type": "string"},
                                                            "minItems": 2,
                                                            "maxItems": 2
                                                        }
                                                    ]
                                                }
                                            }
                                        },
                                        "description": "Array of time dimension objects"
                                    },
                                    "filters": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "member": {"type": "string"},
                                                "operator": {"type": "string"},
                                                "values": {"type": "array"}
                                            }
                                        },
                                        "description": "Array of filter objects"
                                    },
                                    "segments": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Array of segment names"
                                    },
                                    "limit": {
                                        "type": "integer",
                                        "description": "Maximum number of rows to return"
                                    },
                                    "offset": {
                                        "type": "integer",
                                        "description": "Number of rows to skip"
                                    },
                                    "order": {
                                        "type": "object",
                                        "description": "Ordering specification"
                                    }
                                },
                                "additionalProperties": False
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False,
                    },
                },
            ]

        @self.server.list_resources()
        async def handle_list_resources():
            """List available resources."""
            logger.info("Handling list_resources request")
            return []

        @self.server.list_prompts()
        async def handle_list_prompts():
            """List available prompts."""
            logger.info("Handling list_prompts request")
            return []

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]):
            """Handle tool calls."""
            logger.info(f"Handling call_tool request: {name}")
            try:
                if name == "cubejs_meta":
                    return await self._get_meta()
                elif name == "cubejs_load":
                    query = arguments.get("query")
                    if not query:
                        raise ValueError("Query parameter is required")
                    return await self._load_data(query)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            except Exception as e:
                logger.error(f"Error handling tool call {name}: {e}")
                return [{"type": "text", "text": f"Error: {str(e)}"}]

    async def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
        """Make HTTP request to CubeJS API."""
        url = urljoin(f"{self.base_url}/", f"cubejs-api/{endpoint}")
        logger.info(f"Making {method} request to: {url}")
        
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(url, headers=headers)
            elif method == "POST":
                response = await client.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

    async def _get_meta(self):
        """Get CubeJS metadata."""
        try:
            result = await self._make_request("v1/meta")
            return [{"type": "text", "text": json.dumps(result, indent=2)}]
        except Exception as e:
            logger.error(f"Error getting metadata: {e}")
            raise

    async def _load_data(self, query: Dict[str, Any]):
        """Load data using CubeJS query."""
        try:
            # Validate query structure
            self._validate_query(query)
            
            result = await self._make_request("v1/load", method="POST", data={"query": query})
            return [{"type": "text", "text": json.dumps(result, indent=2)}]
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def _validate_query(self, query: Dict[str, Any]) -> None:
        """Validate CubeJS query structure."""
        # Basic validation - ensure query is a dict
        if not isinstance(query, dict):
            raise ValueError("Query must be a dictionary")
        
        # Validate that at least measures or dimensions are specified
        if not any(key in query for key in ["measures", "dimensions", "timeDimensions"]):
            raise ValueError("Query must include at least one of: measures, dimensions, or timeDimensions")
        
        # Validate array fields
        for field in ["measures", "dimensions", "segments"]:
            if field in query and not isinstance(query[field], list):
                raise ValueError(f"{field} must be an array")
        
        # Validate timeDimensions structure
        if "timeDimensions" in query:
            if not isinstance(query["timeDimensions"], list):
                raise ValueError("timeDimensions must be an array")
            for td in query["timeDimensions"]:
                if not isinstance(td, dict) or "dimension" not in td:
                    raise ValueError("Each timeDimension must be an object with a 'dimension' field")
        
        # Validate filters structure
        if "filters" in query:
            if not isinstance(query["filters"], list):
                raise ValueError("filters must be an array")
            for f in query["filters"]:
                if not isinstance(f, dict) or not all(key in f for key in ["member", "operator", "values"]):
                    raise ValueError("Each filter must have 'member', 'operator', and 'values' fields")

    def create_starlette_app(self) -> Starlette:
        """Create a Starlette application that can serve the MCP server with SSE."""
        sse = SseServerTransport("/messages")
        
        async def handle_sse(request: Request) -> None:
            logger.info("SSE connection established")
            async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
            ) as (read_stream, write_stream):
                logger.info("Starting MCP server run loop")
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options(),
                )

        return Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages", app=sse.handle_post_message),
            ],
        )

    async def run_sse(self):
        """Run the MCP server using SSE transport."""
        logger.info(f"Starting CubeJS MCP Server with SSE transport on port {self.port}")
        
        # Create Starlette app with SSE support
        starlette_app = self.create_starlette_app()
        
        # Run the server using uvicorn
        config = uvicorn.Config(
            starlette_app,
            host="0.0.0.0",
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()

async def main():
    """Main entry point."""
    import os
    
    # Get configuration from environment variables
    base_url = os.getenv("CUBEJS_BASE_URL")
    api_token = os.getenv("CUBEJS_API_TOKEN")
    port = int(os.getenv("MCP_PORT", "8000"))
    
    if not base_url:
        logger.error("CUBEJS_BASE_URL environment variable is required")
        sys.exit(1)
    
    server = CubeJSMCPServer(base_url, api_token, port)
    await server.run_sse()

if __name__ == "__main__":
    asyncio.run(main())