# Constants for tool nodes
BORDER_LEN = 96
SYSTEM_MAX_LOOP = 2
BORDER = f"{'=' * BORDER_LEN}"

# MCP Server configuration
MCP_SERVER_PATH = "utils/mcp_server.py"

# Action types
class Actions:
    TOOL = "tool"
    DONE = "done"
    ERROR = "error"
    DEFAULT = "default"
    TOOL_RESULT = "tool_result"

# Shared data keys
class SharedKeys:
    FILE = "file"
    TOOLS = "tools"
    TOOL_INFO = "tool_info"
    ACTION = "action"
    TOOL_NAME = "tool_name"
    PARAMETERS = "parameters"
    THINKING = "thinking"
    TOOL_RESULT = "tool_result"
    RESULT = "result"
    QUESTION = "question" 