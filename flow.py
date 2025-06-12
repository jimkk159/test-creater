from myPocketFlow import AsyncFlow, AsyncParallelBatchFlow
from nodes import AsyncNodeWrapper, GetToolsNode, DecideToolNode, ExecuteToolNode, Analyze_Node, GenerateTestCases, ImplementFunction, RunTests, Revise, ReturnDefaultActionNode

from utils.utils import save_to_file

def Read_and_find_file_flow():
    """Find the file and then read its content"""
    # Create nodes
    get_tools_node = GetToolsNode()
    decide_node = DecideToolNode()
    execute_node = ExecuteToolNode()

    # Error handling
    decide_node - 'error' >> decide_node

    # Create the final node to return "default"
    return_default_node = ReturnDefaultActionNode()

    # Connect nodes
    get_tools_node >> decide_node
    decide_node - "tool" >> execute_node
    execute_node - "tool_result" >> decide_node

    # If decide_node returns anything other than "tool" (like default), go to return_default_node
    decide_node >> return_default_node # This connects the default action of decide_node

    # Create flow starting with test generation
    return AsyncFlow(start=get_tools_node)

# --- Flow Creation ---
def run_test_flow():
    """Creates and returns the parallel translation flow."""
    generate_test_cases = AsyncNodeWrapper(GenerateTestCases(max_retries=3, wait=2))
    implement_function = AsyncNodeWrapper(ImplementFunction(max_retries=5, wait=2))
    run_tests = RunTests()
    revise = AsyncNodeWrapper(Revise(max_retries=5, wait=2))
    return_default_node = AsyncNodeWrapper(ReturnDefaultActionNode())
    
    # Error handling
    generate_test_cases - 'error' >> generate_test_cases
    implement_function - 'error' >> implement_function
    revise - 'error' >> revise
    revise - 'error-implement' >> implement_function 

    generate_test_cases >> implement_function
    implement_function >> run_tests
    run_tests - "failure" >> revise
    run_tests >> return_default_node
    revise >> run_tests
        
    return AsyncFlow(start=generate_test_cases)

class FunctionParallelBatchFlow(AsyncParallelBatchFlow):
    async def prep_async(self, shared):
        # Get all functions from shared store
        functions = shared.get("functions", {})
        # Create a list of params for each function
        return [{"function_name": name, "function_content": content} 
                for name, content in functions.items()]
    async def post_async(self, shared, prep_res, exec_res):
        # Save the test code to a file
        print("🎉All tests passed across all batches!")
        
        test_codes_to_file = ''
        for i, func_name in enumerate(shared["test_code"]):
            test_codes_to_file += f"{shared["test_code"][func_name]}\n\n"
        save_to_file(test_codes_to_file, "final.test.js")

def auto_code_test_generate_flow():
    """Automatically Generate test code and execute the code to ensure the code quality"""

    # Create flows or nodes 
    read_and_find_file_flow = Read_and_find_file_flow()
    analyze_node = AsyncNodeWrapper(Analyze_Node())

    # Create a batch flow for running tests on each function
    function_parallel_batch = FunctionParallelBatchFlow(start=run_test_flow())

    # Connect nodes
    read_and_find_file_flow >> analyze_node
    analyze_node >> function_parallel_batch

    # Create flow starting with test generation
    return AsyncFlow(start=read_and_find_file_flow)