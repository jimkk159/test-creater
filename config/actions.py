"""
Action constants for flow control and node transitions.
"""

class Actions:
    """Core action types for general flow control"""
    TOOL = "tool"
    DONE = "done"
    ERROR = "error"
    DEFAULT = "default"
    SUGGEST = "suggest"
    TOOL_RESULT = "tool_result"

class TestActions:
    """Test-specific action types"""
    PASS = "pass"
    REVISE = "revise"
    ERROR = "error"
    DEFAULT = "default"
    FAILURE = "failure"
    MAX_ITERATION = "max_iteration"

class ToolActions:
    """Tool-specific action types"""
    EXECUTE = "execute"
    VALIDATE = "validate"
    ERROR = "error"
    DEFAULT = "default"