# MCP JSON-RPC Proxy

This is a simple MCP (Model Context Protocol) server that acts as a proxy to a local JSON-RPC server. It exposes the functionality of your JSON-RPC server to MCP clients like Claude Desktop, allowing an AI assistant to interact with your local service.

## Prerequisites

- Python 3.10 or higher
- A running JSON-RPC server on http://localhost:8080
- Claude Desktop (optional, for using with Claude AI)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install mcp[cli] httpx
   ```

## Local JSON-RPC Server

This MCP server is designed to connect to your existing JSON-RPC server at http://localhost:8080. Your server should support the following methods:

- `echo`: Takes a string message parameter and echoes it back
- `get_time`: Takes no parameters and returns the current time

Here are example curl commands that should work with your JSON-RPC server:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "echo", "params": ["planning is everything"], "id": 1}' http://localhost:8080

curl -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method": "get_time", "params": [], "id": 1}' http://localhost:8080
```

## Running the MCP Server

Run the MCP server with:

```bash
python mcp_server.py
```

This starts the server using the stdio transport, which allows it to communicate with MCP clients.

## Using with Claude Desktop

To use this MCP server with Claude Desktop:

1. Make sure Claude Desktop is installed. You can download it from [https://claude.ai/download](https://claude.ai/download).

2. Configure Claude Desktop to use this MCP server by editing the configuration file:

   - On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

3. Add the server configuration:

   ```json
   {
     "mcpServers": {
       "jsonrpc-proxy": {
         "command": "python",
         "args": ["/absolute/path/to/mcp_server.py"]
       }
     }
   }
   ```

   Replace `/absolute/path/to/mcp_server.py` with the actual path to the script.

4. Restart Claude Desktop.

5. In a conversation with Claude, you can now use the tools provided by your JSON-RPC server:
   - `echo`: Sends a message to your server and gets a response
   - `get_time`: Retrieves the current time from your server

## Using with Other MCP Clients

This server can also be used with other MCP clients. For example, you can use the MCP Inspector to test it:

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

## How It Works

1. The MCP server exposes two tools that match the functions of your local JSON-RPC server.
2. When an MCP client (like Claude Desktop) calls one of these tools, the MCP server:
   - Formats a JSON-RPC request
   - Sends it to your local server at http://localhost:8080
   - Receives the response
   - Returns the result back to the MCP client

This creates a bridge between MCP clients and your existing JSON-RPC service.

## Customization

To add more functions from your JSON-RPC server, edit `mcp_server.py` and add new tool functions following the same pattern as the existing ones. 