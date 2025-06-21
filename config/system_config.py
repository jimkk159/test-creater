"""
System configuration constants.
"""


class SystemConfig:
    """System-wide configuration constants"""

    # Core system constants
    BORDER_LEN = 96
    SYSTEM_MAX_LOOP = 2
    BORDER = f"{'=' * BORDER_LEN}"
    BORDER_2 = f"{'-' * BORDER_LEN}"

    # Test configuration
    MAX_ITERATION = 5
    TEST_DIRECTORY = "test"

    # MCP Server configuration
    MCP_SERVER_PATH = "utils/mcp_server.py"


class TestStatus:
    """Test status types"""

    OK = "ok"
    FAIL = "fail"
    PASSED = "passed"
    FAILED = "failed"

