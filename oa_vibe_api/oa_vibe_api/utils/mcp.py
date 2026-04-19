"""MCP (Model Context Protocol) utilities for OA workflow integration."""
from typing import Any, Dict, Optional
import json


class MCPTool:
    """Represents an MCP tool that can be called."""

    def __init__(self, name: str, description: str, input_schema: Dict[str, Any]):
        self.name = name
        self.description = description
        self.input_schema = input_schema

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


class MCPServer:
    """MCP server for OA workflow integration."""

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.tools: Dict[str, MCPTool] = {}

    def register_tool(self, tool: MCPTool):
        """Register a tool with the server."""
        self.tools[tool.name] = tool

    def list_tools(self) -> list[Dict[str, Any]]:
        """List all registered tools."""
        return [tool.to_dict() for tool in self.tools.values()]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a registered tool with arguments."""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}
        # Tool implementation would go here
        return {"result": f"Called {tool_name} with {arguments}"}


# Leave request MCP tools
leave_request_tools = [
    MCPTool(
        name="create_leave_request",
        description="Create a new leave request",
        input_schema={
            "type": "object",
            "properties": {
                "user_id": {"type": "integer"},
                "leave_type": {"type": "string", "enum": ["annual", "sick", "personal"]},
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"},
                "reason": {"type": "string"},
            },
            "required": ["user_id", "leave_type", "start_date", "end_date", "reason"],
        },
    ),
    MCPTool(
        name="approve_leave_request",
        description="Approve a pending leave request",
        input_schema={
            "type": "object",
            "properties": {
                "leave_id": {"type": "integer"},
                "approver_id": {"type": "integer"},
                "comment": {"type": "string"},
            },
            "required": ["leave_id", "approver_id"],
        },
    ),
    MCPTool(
        name="reject_leave_request",
        description="Reject a pending leave request",
        input_schema={
            "type": "object",
            "properties": {
                "leave_id": {"type": "integer"},
                "approver_id": {"type": "integer"},
                "reason": {"type": "string"},
            },
            "required": ["leave_id", "approver_id"],
        },
    ),
    MCPTool(
        name="get_leave_request_status",
        description="Get the status of a leave request",
        input_schema={
            "type": "object",
            "properties": {
                "leave_id": {"type": "integer"},
            },
            "required": ["leave_id"],
        },
    ),
]


def get_leave_request_mcp_server() -> MCPServer:
    """Get MCP server configured for leave request workflow."""
    server = MCPServer(name="oa_leave_request", version="1.0.0")
    for tool in leave_request_tools:
        server.register_tool(tool)
    return server
