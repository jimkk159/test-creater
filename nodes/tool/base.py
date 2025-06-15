from myPocketFlow import Node, AsyncNode
from ..constants import BORDER, SYSTEM_MAX_LOOP
from utils.utils import handle_max_iteration_error

class BaseToolNode(Node):
    """Base class for tool-related nodes"""
    
    def handle_error(self, shared, response):
        """Handle error responses"""
        return handle_max_iteration_error(
            shared, response, BORDER, SYSTEM_MAX_LOOP, ["decide"]
        )

class BaseAsyncToolNode(AsyncNode):
    """Base class for async tool-related nodes"""
    
    async def handle_error_async(self, shared, response):
        """Handle error responses asynchronously"""
        return await handle_max_iteration_error(
            shared, response, BORDER, SYSTEM_MAX_LOOP, ["decide"]
        ) 