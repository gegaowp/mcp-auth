# MCP JSON-RPC Proxy

This is a simple MCP (Model Context Protocol) server that acts as a proxy to a local JSON-RPC server. It exposes the functionality of your JSON-RPC server to MCP clients like Claude Desktop, allowing an AI assistant to interact with your local service.

running the other simple server
```
python3 /Users/ggaowp/Desktop/simple_server/simple_server.py
```

venv
```
./setup.sh
source venv/bin/activate
```

run both server and client with a CLI interface
```
./venv/bin/python ./mcp_server.py
./venv/bin/python ./mcp_client.py
```