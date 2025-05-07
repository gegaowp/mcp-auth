#!/usr/bin/env python3

import httpx
import json
from mcp.server.fastmcp import FastMCP

# Initialize an MCP server named "jsonrpc-proxy"
mcp = FastMCP("jsonrpc-proxy")

# Local JSON-RPC server endpoint
JSONRPC_SERVER = "http://localhost:8080"

async def call_jsonrpc(method, params):
    """Helper function to call the local JSON-RPC server."""
    
    # Build the JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    
    # Make the request to the local server
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                JSONRPC_SERVER, 
                json=request,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Error calling JSON-RPC server: {str(e)}"}

@mcp.tool()
async def echo(message: str) -> str:
    """Echo back a message.
    
    Args:
        message: The message to echo back
    """
    response = await call_jsonrpc("echo", [message])
    
    if "error" in response:
        return f"Error: {response['error']}"
    
    if "result" in response:
        return f"Echo response: {response['result']}"
    
    return "Unexpected response format"

@mcp.tool()
async def get_time() -> str:
    """Get the current server time.
    """
    response = await call_jsonrpc("get_time", [])
    
    if "error" in response:
        return f"Error: {response['error']}"
    
    if "result" in response:
        return f"Current server time: {response['result']}"
    
    return "Unexpected response format"

if __name__ == "__main__":
    # Initialize and run the server with stdio transport
    mcp.run(transport='stdio') 