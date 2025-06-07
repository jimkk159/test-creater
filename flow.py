from pocketflow import Flow
from nodes import GetToolsNode, DecideToolNode, ExecuteToolNode, Analyze_Node, GenerateTestCases, ImplementFunction, RunTests, Revise, ReturnDefaultActionNode

def Read_and_find_file_flow():
    """Find the file and then read its content"""
    # Create nodes
    get_tools_node = GetToolsNode()
    decide_node = DecideToolNode()
    execute_node = ExecuteToolNode()

    # Create the final node to return "default"
    return_default_node = ReturnDefaultActionNode()

    # Connect nodes
    get_tools_node - "decide" >> decide_node
    decide_node - "tool" >> execute_node
    execute_node - "tool_result" >> decide_node
    # If decide_node returns anything other than "tool" (like default), go to return_default_node
    decide_node >> return_default_node # This connects the default action of decide_node


    # Create flow starting with test generation
    return Flow(start=get_tools_node)

def auto_code_test_generate_flow():
    """Automatically Generate test code and execute the code to ensure the code quality"""

    # Create flows or nodes 
    read_and_find_file_flow = Read_and_find_file_flow()
    analyze_node = Analyze_Node()
    generate_test_cases = GenerateTestCases()
    implement_function = ImplementFunction()
    run_tests = RunTests()
    revise = Revise()
    return_default_node = ReturnDefaultActionNode()

    # Connect nodes
    read_and_find_file_flow >> analyze_node
    analyze_node >> generate_test_cases
    generate_test_cases >> implement_function
    implement_function >> run_tests
    run_tests - "failure" >> revise
    # run_tests - "success"  >> return_default_node
    # revise >> run_tests

    # Create flow starting with test generation
    flow = Flow(start=revise)
    return flow 