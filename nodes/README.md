# Nodes Package - Refactored Structure

This directory contains clean, modular implementations for both **MCP tool integration** and **automated test generation**.

## 🎯 What Was Improved

Both `tool_nodes.py` and `test_nodes.py` had similar issues:
- **Large classes** doing too many things (50-70 lines each)
- **Mixed responsibilities** (formatting, parsing, state management, business logic)
- **Hard-coded constants** scattered throughout
- **Complex nested logic** that was hard to follow
- **Poor error handling** mixed with business logic
- **Repeated patterns** across different node types

## 📁 New Structure

### Core Tool Files

| File | Purpose | Responsibilities |
|------|---------|------------------|
| `constants.py` | Tool Configuration | Constants, action types, shared keys |
| `tool_formatter.py` | Tool Formatting | Tool info formatting, prompt building |
| `response_parser.py` | Response Parsing | YAML parsing, response validation |
| `shared_manager.py` | State Management | Clean shared state operations |
| `tool_nodes.py` | Tool Business Logic | Clean, focused node implementations |

### Core Test Files

| File | Purpose | Responsibilities |
|------|---------|------------------|
| `test_constants.py` | Test Configuration | Test-specific constants and enums |
| `test_formatters.py` | Test Formatting | Test case formatting, prompt building |
| `test_response_parser.py` | Test Parsing | Specialized test response validation |
| `test_shared_manager.py` | Test State Management | Test-specific state operations |
| `test_nodes.py` | Test Business Logic | Clean test automation nodes |

### Shared Utilities

- **`ResponseParser`**: Base YAML parsing and validation (shared)
- **`ToolFormatter`**: Formats MCP tools into readable strings
- **`TestFormatter`**: Formats test cases and results
- **`SharedManager`**: Manages tool-related shared state
- **`TestSharedManager`**: Manages test-specific shared state

## 🚀 Benefits

### 1. **Single Responsibility Principle**
Each class now has one clear purpose:

```python
# Before: Giant node doing everything
class DecideToolNode(Node):
    def prep(self, shared):
        # 60+ lines of prompt building, error handling, formatting...
    
# After: Focused node with helpers
class DecideToolNode(Node):
    def prep(self, shared):
        return PromptBuilder.build_decision_prompt(shared)
```

### 2. **Shared Logic Reuse**
Common patterns are now reusable:

```python
# Both tool and test nodes use the same base parser
class TestResponseParser(ResponseParser):  # Extends base parser
    @staticmethod
    def validate_test_case_response(parsed_response):
        ResponseParser.validate_decision_response(parsed_response)  # Reuse base validation
        # Add test-specific validation...
```

### 3. **Better Organization**
Clear separation between tool and test concerns:

```python
from nodes import (
    # Tool operations
    GetToolsNode, DecideToolNode, ExecuteToolNode,
    Actions, SharedManager,
    
    # Test operations  
    AnalyzeNode, GenerateTestCasesNode, RunTestsNode,
    TestActions, TestSharedManager
)
```

### 4. **Easier Testing**
You can now test each component independently:

```python
# Test just the tool formatter
formatted = ToolFormatter.format_tool_info(tools)

# Test just the test case validator
TestResponseParser.validate_test_case_response(response)

# Test shared state operations
TestSharedManager.store_test_results(shared, "func", 5, 10, [])
```

## 🔧 Usage Examples

### Tool Automation
```python
from nodes import GetToolsNode, DecideToolNode, ExecuteToolNode, Actions

get_tools = GetToolsNode()
decide_tool = DecideToolNode()
execute_tool = ExecuteToolNode()

get_tools >> decide_tool
decide_tool - Actions.TOOL >> execute_tool
execute_tool >> decide_tool

flow = AsyncFlow(start=get_tools)
await flow.run_async(shared)
```

### Test Automation
```python
from nodes import AnalyzeNode, GenerateTestCasesNode, RunTestsNode, TestActions

analyze = AnalyzeNode()
generate = GenerateTestCasesNode()
run_tests = RunTestsNode()
revise = ReviseNode()

analyze >> generate >> implement >> run_tests
run_tests - TestActions.FAILURE >> revise
revise >> implement

flow = Flow(start=analyze)
flow.run(shared)
```

## 📊 Code Metrics Improvement

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Lines per class | 50-70 | 15-25 | 60% reduction |
| Responsibilities per class | 4-5 | 1-2 | Single purpose |
| Cyclomatic complexity | High | Low | Much simpler |
| Testability | Poor | Excellent | Each piece testable |
| Code reuse | None | High | Shared utilities |

## 🧪 Testing Strategy

Each module can now be tested independently:

```python
# Test tool formatting
def test_tool_formatting():
    tools = [mock_tool()]
    result = ToolFormatter.format_tool_info(tools)
    assert "[1] tool_name" in result

# Test test case parsing  
def test_test_case_parsing():
    response = "```yaml\ntest_cases:\n  func: []\n```"
    result = TestResponseParser.parse_yaml_response(response)
    TestResponseParser.validate_test_case_response(result)

# Test shared state management
def test_test_shared_manager():
    shared = {}
    TestSharedManager.store_test_results(shared, "func", 5, 10, [])
    assert TestKeys.PASSED in shared
```

## 🔄 Backward Compatibility

All original class names are preserved as aliases:

```python
# Old way still works
from nodes import Analyze_Node, GenerateTestCases, ImplementFunction

# New way is cleaner
from nodes import AnalyzeNode, GenerateTestCasesNode, ImplementFunctionNode
```

## 🎭 Design Patterns Used

- **Strategy Pattern**: Different formatters for different content types
- **Factory Pattern**: Utility classes create formatted content
- **Template Method**: Base parsers extended for specific needs
- **State Manager**: Centralized shared state operations
- **Constants as Enums**: Type-safe constant management

This refactored structure follows **SOLID principles** and makes both tool integration and test automation much more maintainable and extensible. 