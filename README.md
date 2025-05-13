# MCP JSON-RPC Proxy

A Model Context Protocol (MCP) server that handles embedded wallet and auth token orchestration, as well as a CLI client.

## Features

- Exposes your JSON-RPC methods as MCP tools
- Includes both server and client components
- Handles token-based authentication
- Provides a simple CLI interface for testing

## Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`

## Setup

1. Clone the repository and navigate to the project directory:
   ```
   git clone https://github.com/gegaowp/mcp-auth.git
   cd mcp-auth
   ```

2. Run the setup script to create a virtual environment and install dependencies:
   ```
   ./setup.sh
   ```

3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

## Usage

### Running the JSON-RPC Server

First, start your local JSON-RPC server. The MCP server is configured to connect to `http://localhost:8080` by default.

```
python3 /path/to/your/json_rpc_server.py
```

### Running the MCP Server

Start the MCP server to expose your JSON-RPC methods as MCP tools:

```
./venv/bin/python ./mcp_server.py
```

### Using the CLI Client

For testing and development, use the included CLI client:

```
./venv/bin/python ./mcp_client.py
```

The client provides an interactive command-line interface with the following commands:
- `help` - Show available commands
- `list` - List available tools
- `echo <message>` - Test the echo functionality
- `time` - Get the current server time
- `purchase_token` - Purchase a JWT authentication token
- `exit` - Exit the client

## Available MCP Tools

The server exposes the following tools:

1. `purchase_token` - Purchase a JWT token for authentication
2. `echo` - Echo back a message (requires authentication)
3. `get_time` - Get the current server time (requires authentication)

## Integration with Claude Desktop

Connect Claude Desktop to your MCP server to allow Claude to interact with your local JSON-RPC services.