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
                headers={"Content-Type": "application/json"},
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling JSON-RPC server: {str(e)}")
            return {"error": f"Error calling JSON-RPC server: {str(e)}"}

@mcp.tool()
async def echo(message: str) -> str:
    """Echo back a message.
    
    Args:
        message: The message to echo back
    """
    try:
        response = await call_jsonrpc("echo", [message])
        
        if "error" in response:
            return f"Error: {response['error']}"
        
        if "result" in response:
            # Handle both string and array results
            result = response['result']
            if isinstance(result, list) and len(result) > 0:
                return f"Echo response: {result[0]}"
            return f"Echo response: {result}"
        
        return "Unexpected response format"
    except Exception as e:
        print(f"Error in echo tool: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
async def get_time() -> str:
    """Get the current server time.
    """
    try:
        response = await call_jsonrpc("get_time", [])
        
        if "error" in response:
            return f"Error: {response['error']}"
        
        if "result" in response:
            return f"Current server time: {response['result']}"
        
        return "Unexpected response format"
    except Exception as e:
        print(f"Error in get_time tool: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Enable debug logging
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    print("MCP server starting - connecting to JSON-RPC server at:", JSONRPC_SERVER)
    # Initialize and run the server with stdio transport
    mcp.run(transport='stdio') 