import re
import os
import shutil
import asyncio
import subprocess
from config import SharedKeys, SystemConfig
from datetime import datetime
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def get_git_hash():
    """Get the current git commit hash."""
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
    except:
        return 'nogit'

def get_next_counter(base_dir):
    """Get and increment the counter for file naming."""
    counter_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), base_dir, '.counter')
    
    try:
        with open(counter_file, 'r') as f:
            counter = int(f.read().strip())
    except (FileNotFoundError, ValueError):
        counter = 0
    
    counter += 1
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(counter_file), exist_ok=True)
    
    # Save the new counter
    with open(counter_file, 'w') as f:
        f.write(str(counter))
    
    return counter

def copy_file(source, filename, base_dir=SystemConfig.TEST_DIRECTORY, prefix=""):
    # Create absolute path for the directory
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), base_dir)
    os.makedirs(save_dir, exist_ok=True)

    # Generate date in YYYYMMDD format and get next counter
    date_str = datetime.now().strftime('%Y%m%d')
    # counter = get_next_counter(base_dir)
    git_hash = get_git_hash()
    
    # Create full filename with prefix, date, git hash and counter
    full_filename = f"{prefix}_{date_str}_{git_hash}.{filename}"
    
    # Create full file path
    full_path = os.path.join(save_dir, full_filename)
    
    # Write the file
    shutil.copyfile(source, full_path)
    
    return full_path

def save_to_file(data, filename, base_dir=SystemConfig.TEST_DIRECTORY, prefix=""):
    """
    Save data to a file, creating the directory if it doesn't exist.
    
    Args:
        data: The data to save
        filename: The name of the file (without extension)
        base_dir: The base directory to save in (default: "test")
        prefix: Prefix for the filename (default: "")
    
    Returns:
        str: The full path where the file was saved
    """
    # Create absolute path for the directory
    save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), base_dir)
    os.makedirs(save_dir, exist_ok=True)

    # Generate date in YYYYMMDD format and get next counter
    date_str = datetime.now().strftime('%Y%m%d')
    # counter = get_next_counter(base_dir)
    git_hash = get_git_hash()
    
    # Create full filename with prefix, date, git hash and counter
    full_filename = f"{prefix}_{date_str}_{git_hash}.{filename}"
    
    # Create full file path
    full_path = os.path.join(save_dir, full_filename)

    # Write the file
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(data)
    
    return full_path

    
def get_tools(server_script_path):
    """Get available tools from an MCP server.
    """
    async def _get_tools():
        server_params = StdioServerParameters(
            command="python3",
            args=[server_script_path]
        )
        
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools_response = await session.list_tools()
                return tools_response.tools
    
    return _get_tools()
    
async def call_tool(server_script_path=None, tool_name=None, arguments=None):
    
    """Call a tool on an MCP server.
    """
    server_params = StdioServerParameters(
        command="python3",
        args=[server_script_path]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text

def extract_describe_blocks(js_code: str):
    blocks = []
    pattern = re.compile(r'describe\(([^)]+)\)\s*=>\s*{')

    start_positions = [m.start() for m in pattern.finditer(js_code)]
    for start in start_positions:
        i = start
        brace_count = 0
        in_block = False

        while i < len(js_code):
            if js_code[i] == '{':
                brace_count += 1
                in_block = True
            elif js_code[i] == '}':
                brace_count -= 1
                if brace_count == 0 and in_block:
                    # Look ahead for closing ');'
                    end = i

                    while end < len(js_code) and not js_code[end:end+2] == ');':
                        end += 1
                    blocks.append(js_code[start:end+2])  # Include ');'
                    break
            i += 1

    return blocks

async def main():
    # Find available tools
    print("=== Finding available tools ===")
    tools = await get_tools("mcp_server.py")

    # Print tool information nicely formatted
    for i, tool in enumerate(tools, 1):
        print(f"\nTool {i}: {tool.name}")
        print("=" * (len(tool.name) + 8))
        print(f"Description: {tool.description}")
        
        # Parameters section
        print("Parameters:")
        properties = tool.inputSchema.get('properties', {})
        required = tool.inputSchema.get('required', [])
        
        # No parameters case
        if not properties:
            print("  None")
        
        # Print each parameter with its details
        for param_name, param_info in properties.items():
            param_type = param_info.get('type', 'unknown')
            req_status = "(Required)" if param_name in required else "(Optional)"
            print(f"  • {param_name}: {param_type} {req_status}")
    
    # Call a tool
    print("\n=== Calling the read file tool ===")
    result = await call_tool("mcp_server.py", "read_file_tool", {"path": "test.txt"})
    print(f"Result : {result}")

    print("=== Get directory structure ===")
    result = await call_tool("mcp_server.py", "read_directory_tree_tool", {"path": "."})
    print(f"Result : {result}")

def cleanup_temp_files(shared, target):
    """
    Clean up temporary files stored in shared["temp_file_paths"].
    
    Args:
        shared: The shared context dictionary containing temp_file_paths
        
    Returns:
        list: List of files that were successfully deleted
    """
    deleted_files = []
    if not target or not isinstance(target, str): 
        return

    if target in shared:
        for file_path in shared[SharedKeys.TEMP_FILE_PATHS].values():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_files.append(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
    return deleted_files

def get_error_value(shared, keys):
    current = shared
    for i, key in enumerate(keys):
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    return current

def get_error_prompt(shared, keys):
    error = get_error_value(shared, keys)
    error_prompt = ""
    if error:
        error_prompt = f"""
        ### PREVIOUS ERROR

        {error}
        """
    return error_prompt

def set_nested_value(d, keys, value=None, increment=False, default=0):
    """
    Traverse or create nested dicts in d using keys. If increment is True, increment the final value (assumed int), else set it to value.
    Returns the final value after operation.
    """
    current = d
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    final_key = keys[-1]
    if increment:
        if final_key not in current:
            current[final_key] = default
        else:
            current[final_key] += 1
        return current[final_key]
    else:
        current[final_key] = value
        return current[final_key]

def handle_max_iteration_error(shared, exec_res, border, max_loop, keys=[], return_key='error'):
    if len(keys) == 0:
        return 'default'

    print(border)
    # record the max loop number and decide if human should be called
    if SharedKeys.MAX_LOOP not in shared:
        shared[SharedKeys.MAX_LOOP] = {}
    
    # Navigate through the hierarchy using keys for max_loop
    count = set_nested_value(shared[SharedKeys.MAX_LOOP], keys, increment=True, default=0)
    
    if count >= max_loop:
        print(border)
        print("💀 Max loop reached. Returning 'human' action.")
        return "human"

    # record the error
    if return_key not in shared:
        shared[return_key] = {}

    print(exec_res)
    print("🔁 Max retries reached or error in exec. Returning 'error' action.", exec_res[return_key])
    set_nested_value(shared[return_key], keys, value=exec_res[return_key])
    return return_key

if __name__ == "__main__":
    asyncio.run(main())


