from pocketflow import Flow
from nodes import GetToolsNode, DecideToolNode, ExecuteToolNode

def create_code_generator_flow():
    """Creates and returns the code generator flow."""
    # Create nodes
    get_tools_node = GetToolsNode()
    decide_node = DecideToolNode()
    execute_node = ExecuteToolNode()
    
    # Connect nodes
    get_tools_node - "decide" >> decide_node
    decide_node - "tool" >> execute_node
    execute_node - "tool_result" >> decide_node

    # Create flow starting with test generation
    flow = Flow(start=get_tools_node)
    return flow 