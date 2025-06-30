#!/usr/bin/env python3
"""
Run script for the Vibe Coder Stack Planner MCP Server
"""

import asyncio
from vibe_stack_planner import mcp

def main():
    """Main entry point"""
    mcp.run()

if __name__ == "__main__":
    main()