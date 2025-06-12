import os
import yaml
from myPocketFlow import Node, AsyncNode
from utils.call_llm.open_ai import call_llm
from utils.utils import get_tools, call_tool

BORDER_LEN = 96
border = f"{"=" * BORDER_LEN}"
allowed_dir = os.environ.get("ALLOW_READ_FILE_PATH")

class GetToolsNode(AsyncNode):
    async def prep_async(self, shared):
        """Initialize and get tools"""
        print("🔍 Getting available tools...")
        # Path to the mcp server script relative to the workspace root
        relative_server_path = "utils/mcp_server.py"

        # Get the absolute path of the workspace root
        workspace_root = os.getcwd() 
        
        # Construct the absolute path to the server script
        absolute_server_path = os.path.join(workspace_root, relative_server_path)
        
        # Check if the absolute path starts with the allowed directory prefix
        if not absolute_server_path.startswith(allowed_dir):
             raise ValueError(f"Error: The mcp_server.py script ({absolute_server_path}) is not located within the allowed directory ({allowed_dir}).")

        # If the check passes, return the relative path
        return relative_server_path

    async def exec_async(self, server_path):
        """Retrieve tools from the MCP server"""
        tools = await get_tools(server_path)
        return tools

    async def post_async(self, shared, prep_res, exec_res):
        """Store tools and process to yamlResult node"""
        tools = exec_res
        shared["file"]["tools"] = tools
        # Format tool information for later use
        tool_info = []
        for i, tool in enumerate(tools, 1):
            properties = tool.inputSchema.get('properties', {})
            required = tool.inputSchema.get('required', [])
            
            params = []
            for param_name, param_info in properties.items():
                param_type = param_info.get('type', 'unknown')
                req_status = "(Required)" if param_name in required else "(Optional)"
                params.append(f"    - {param_name} ({param_type}): {req_status}")
            
            tool_info.append(f"[{i}] {tool.name}\n  Description: {tool.description}\n  Parameters:\n" + "\n".join(params))
        
        shared["file"]["tool_info"] = "\n".join(tool_info)

class DecideToolNode(Node):
    def prep(self, shared):
        """Prepare the prompt for LLM to process the question"""
        tool_info = shared["file"]["tool_info"]

        question = shared["question"]   
        pre_task_info = ""
        if  "file" in shared and "action" in shared["file"] : 
            pre_task_info = f"""
                ### PREVIOUS ACTION
                {shared["file"].get("action", "")}

                ### PREVIOUS TOOL
                {shared["file"].get("tool_name", "")}

                ### PREVIOUS PARAMETERS
                {shared["file"].get("parameters", "")}

                ### PREVIOUS ACTION RESULT
                {shared["file"].get("tool_result", "")}
            """ 

        prompt = (f"""
### CONTEXT
You are an assistant that can use tools via Model Context Protocol (MCP).

### ACTION SPACE
{tool_info}

### TASK
Answer this question: "{question}"

{pre_task_info}

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
        )
        return prompt

    def exec(self, prompt):
        """Call LLM to process the question and decide which tool to use"""
        print(border)
        print("🤔 Analyzing question and deciding which tool to use...")
        response = call_llm(prompt)
        return response

    def post(self, shared, prep_res, exec_res):
        """Extract yamlResult from YAML and save to shared context"""
        try:
            yaml_str = exec_res.split("```yaml")[1].split("```")[0].strip()
            yamlResult = yaml.safe_load(yaml_str)
            
            shared["file"]["action"] = yamlResult.get("action", "")
            shared["file"]["tool_name"] = yamlResult.get("tool", "")
            shared["file"]["parameters"] = yamlResult.get("parameters", "")
            shared["file"]["thinking"] = yamlResult.get("thinking", "")
            print(border)
            print(f"🎬 Selected action: {shared["file"]["action"]}")

            if shared["file"]["action"] == 'done':
                answer = f"✅ FILE CONTENT:\n{shared["file"]['tool_result']}".rstrip('\n')
                shared["file"]["result"] = answer
                print(border)
                print(answer)
                return "default"
            elif shared["file"]["action"] == 'tool':
                print(f"💡 Selected tool: {yamlResult['tool']}")
                print(f"🔢 Extracted parameters: {yamlResult['parameters']}")
                return "tool"
            return "error"
            
        except Exception as e:
            print(f"❌ Error parsing LLM response on reading file: {e}")
            print("Raw response:", exec_res)
            return None

class ExecuteToolNode(AsyncNode):
    async def prep_async(self, shared):
        """Prepare tool execution parameters"""
        return shared["file"]["tool_name"], shared["file"]["parameters"]

    async def exec_async(self, inputs):
        """Execute the chosen tool"""
        tool_name, parameters = inputs
        print(f"🔧 Executing tool '{tool_name}' with parameters: {parameters}")
        result = await call_tool("utils/mcp_server.py", tool_name, parameters)
        return result

    async def post_async(self, shared, prep_res, exec_res):
        shared["file"]["tool_result"] = exec_res
        return "tool_result" 