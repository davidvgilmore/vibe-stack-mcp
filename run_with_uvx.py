#!/usr/bin/env python3
"""
Entry point for running the MCP server with uvx
"""

import os
import sys

# Change to the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

# Add project directory to Python path
sys.path.insert(0, project_dir)

# Import and run the server
from vibe_stack_planner import mcp

if __name__ == "__main__":
    mcp.run()