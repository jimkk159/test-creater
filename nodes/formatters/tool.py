from ..constants import SharedKeys

class ToolFormatter:
    @staticmethod
    def format_tool_info(tools):
        """Format tools into readable information string"""
        tool_info = []
        for i, tool in enumerate(tools, 1):
            properties = tool.inputSchema.get('properties', {})
            required = tool.inputSchema.get('required', [])
            
            params = []
            for param_name, param_info in properties.items():
                param_type = param_info.get('type', 'unknown')
                req_status = "(Required)" if param_name in required else "(Optional)"
                params.append(f"    - {param_name} ({param_type}): {req_status}")
            
            tool_info.append(
                f"[{i}] {tool.name}\n"
                f"  Description: {tool.description}\n"
                f"  Parameters:\n" + "\n".join(params)
            )
        
        return "\n".join(tool_info)

class PromptBuilder:
    @staticmethod
    def build_decision_prompt(shared):
        """Build the prompt for tool decision"""
        from utils.utils import get_error_prompt
        
        tool_info = shared[SharedKeys.FILE][SharedKeys.TOOL_INFO]
        question = shared[SharedKeys.QUESTION]
        
        pre_task_info = PromptBuilder._get_previous_action_info(shared)
        error_prompt = get_error_prompt(shared, ["error", 'decide'])

        return f"""
### CONTEXT
You are an assistant that can use tools via Model Context Protocol (MCP).

### ACTION SPACE
{tool_info}

### TASK
Answer this question: "{question}"

{pre_task_info}

{error_prompt}

## NEXT ACTION
Analyze the question, 
base on the previous action, (if there has any)
decide next action to exec.

Your action choice: [tool, done, error]

- tool:
    Extract any numbers or parameters, and decide which tool to use.
    Sometime, you need to call tool multiple times.

- done:
    This action means the question has been fulfilled

- error:
    Something went wrong, and you need human to solve the problem

Return your response in this format:

```yaml
action: <name of the action>
thinking: |
    <your step-by-step reasoning about what the question is asking and what numbers to extract>
tool: <name of the tool to use>
reason: <why you chose this tool>
parameters:
    <parameter_name>: <parameter_value>
    <parameter_name>: <parameter_value>
```
IMPORTANT: 
1. Extract numbers from the question properly
2. Use proper indentation (4 spaces) for multi-line fields
3. Use the | character for multi-line text fields
4. If you already got the answer, just choice the done action.
"""

    @staticmethod
    def _get_previous_action_info(shared):
        """Get previous action information if available"""
        if SharedKeys.FILE in shared and SharedKeys.ACTION in shared[SharedKeys.FILE]:
            return f"""
                ### PREVIOUS ACTION
                {shared[SharedKeys.FILE].get(SharedKeys.ACTION, "")}

                ### PREVIOUS TOOL
                {shared[SharedKeys.FILE].get(SharedKeys.TOOL_NAME, "")}

                ### PREVIOUS PARAMETERS
                {shared[SharedKeys.FILE].get(SharedKeys.PARAMETERS, "")}

                ### PREVIOUS ACTION RESULT
                {shared[SharedKeys.FILE].get(SharedKeys.TOOL_RESULT, "")}
            """
        return "" 