#!/usr/bin/env python3

import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# ANSI colors for better output
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.tools = []
        
    async def connect(self):
        """Connect to the MCP server"""
        try:
            # Set up server parameters - connect to existing server
            server_params = StdioServerParameters(
                command="python",
                args=["mcp_server.py"],
                client_info={
                    "name": "simple-mcp-client",
                    "version": "0.1.0"
                }
            )
            
            # Create the client session with timeout
            print(f"{BLUE}Connecting to MCP server...{RESET}")
            try:
                async with asyncio.timeout(5):  # 5 second timeout
                    stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
                    self.stdio, self.write = stdio_transport
                    self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

                    await self.session.initialize()

                    response = await self.session.list_tools()
                    tools = response.tools
                    print(f"{GREEN}Connected to server, listing tools...{RESET}")
                    print("\nConnected to server with tools:", [tool.name for tool in tools])
                    self.tools = tools
            except asyncio.TimeoutError:
                print(f"{RED}Timeout while connecting to server. Is the server running?{RESET}")
                return False
            
            print(f"{GREEN}Successfully connected to MCP server{RESET}")
            return True
            
        except Exception as e:
            print(f"{RED}Error connecting to server: {str(e)}{RESET}")
            return False
            
    async def list_tools(self):
        """List available tools from the server"""
        if not self.session:
            print(f"{RED}Not connected to server{RESET}")
            return
            
        try:
            if self.tools:
                print(f"\n{GREEN}Available tools:{RESET}")
                for i, tool in enumerate(self.tools, 1):
                    print(f"{BOLD}{i}.{RESET} {tool.name}: {tool.description}")
            else:
                print(f"{YELLOW}No tools available{RESET}")
        except Exception as e:
            print(f"{RED}Error listing tools: {str(e)}{RESET}")
            
    async def call_tool(self, name: str, **kwargs):
        """Call a specific tool"""
        if not self.session:
            print(f"{RED}Not connected to server{RESET}")
            return
            
        try:
            print(f"{BLUE}Calling tool '{name}' with args: {kwargs}{RESET}")
            response = await asyncio.wait_for(
                self.session.call_tool(name, kwargs),
                timeout=5  # 5 second timeout for tool calls
            )
            
            if response and response.content:
                print(f"{GREEN}Tool response:{RESET}")
                for content in response.content:
                    print(f"{BOLD}{content.text}{RESET}")
            else:
                print(f"{RED}No response from tool{RESET}")
                
        except asyncio.TimeoutError:
            print(f"{RED}Timeout while calling tool{RESET}")
        except Exception as e:
            print(f"{RED}Error calling tool: {str(e)}{RESET}")
            
    async def interactive_cli(self):
        """Run an interactive CLI"""
        print(f"\n{GREEN}{BOLD}=== MCP Client ==={RESET}")
        print(f"{BLUE}Type 'help' for usage information or 'exit' to quit{RESET}")
        
        while True:
            try:
                command = input(f"\n{BOLD}mcp> {RESET}").strip()
                
                if not command:
                    continue
                    
                if command.lower() == 'exit':
                    break
                    
                elif command.lower() == 'help':
                    print(f"\n{BLUE}Available commands:{RESET}")
                    print("  help              - Show this help message")
                    print("  list              - List available tools")
                    print("  echo <message>    - Call echo tool")
                    print("  time              - Get current time")
                    print("  exit              - Exit the client")
                    
                elif command.lower() == 'list':
                    await self.list_tools()
                    
                elif command.lower().startswith('echo '):
                    message = command[5:].strip()
                    await self.call_tool('echo', message=message)
                    
                elif command.lower() == 'time':
                    await self.call_tool('get_time')
                    
                else:
                    print(f"{RED}Unknown command. Type 'help' for usage information.{RESET}")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue
                
            except Exception as e:
                print(f"{RED}Error: {str(e)}{RESET}")
            
    async def cleanup(self):
        """Clean up resources"""
        if self.exit_stack:
            await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    
    try:
        # Connect to server
        if not await client.connect():
            return
            
        # Run interactive CLI
        await client.interactive_cli()
        
    finally:
        await client.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{BLUE}Goodbye!{RESET}") 