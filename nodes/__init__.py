"""
Tool nodes package for MCP integration and test automation.

This package provides clean, modular nodes for tool discovery, decision making,
tool execution, and comprehensive test automation using the Model Context Protocol (MCP).
"""

import os
from dotenv import load_dotenv
from .base_nodes import AsyncNodeWrapper, ReturnDefaultActionNode
from .tool_nodes import GetToolsNode, DecideToolNode, ExecuteToolNode
from .test_nodes import AnalyzeNode, GenerateTestCasesNode, ImplementFunctionNode, RunTestsNode, ReviseNode

# Backward compatibility aliases
from .test_nodes import Analyze_Node, GenerateTestCases, ImplementFunction, RunTests, Revise

# Constants and utilities
from .constants import Actions, SharedKeys, BORDER, MCP_SERVER_PATH
from .tool_formatter import ToolFormatter, PromptBuilder
from .response_parser import ResponseParser
from .shared_manager import SharedManager

# Test-specific constants and utilities
from .test_constants import TestActions, TestKeys, MAX_ITERATION, TestStatus
from .test_formatters import TestFormatter, TestPromptBuilder
from .test_response_parser import TestResponseParser
from .test_shared_manager import TestSharedManager

load_dotenv()

MAX_ITERATION = 3
BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"
allowed_dir=os.environ.get("ALLOW_READ_FILE_PATH")

__all__ = [
    # Base nodes
    'AsyncNodeWrapper',
    'ReturnDefaultActionNode',
    
    # Tool nodes
    'GetToolsNode',
    'DecideToolNode',
    'ExecuteToolNode',
    
    # Test nodes (new naming)
    'AnalyzeNode',
    'GenerateTestCasesNode', 
    'ImplementFunctionNode',
    'RunTestsNode',
    'ReviseNode',
    
    # Test nodes (backward compatibility)
    'Analyze_Node',
    'GenerateTestCases',
    'ImplementFunction',
    'RunTests',
    'Revise',
    
    # Tool constants and utilities
    'Actions',
    'SharedKeys',
    'BORDER',
    'MCP_SERVER_PATH',
    'ToolFormatter',
    'PromptBuilder',
    'ResponseParser',
    'SharedManager',
    
    # Test constants and utilities
    'TestActions',
    'TestKeys',
    'MAX_ITERATION',
    'TestStatus',
    'TestFormatter',
    'TestPromptBuilder',
    'TestResponseParser',
    'TestSharedManager',
] 