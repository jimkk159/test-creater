import asyncio
from myPocketFlow import Node, AsyncNode

class AsyncNodeWrapper(AsyncNode):
    def __init__(self, sync_node, max_retries=1, wait=0):
        super().__init__(max_retries=max_retries, wait=wait)
        self.sync_node = sync_node

    async def prep_async(self, shared):
        # Pass params to sync node
        self.sync_node.params = self.params
        # Run sync prep in a thread pool to avoid blocking
        return await asyncio.to_thread(self.sync_node.prep, shared)

    async def exec_async(self, prep_res):
        # Run sync exec in a thread pool
        return await asyncio.to_thread(self.sync_node.exec, prep_res)

    async def post_async(self, shared, prep_res, exec_res):
        # Run sync post in a thread pool
        self.sync_node.params = self.params
        return await asyncio.to_thread(self.sync_node.post, shared, prep_res, exec_res)

    async def exec_fallback_async(self, prep_res, exc): 
        return await asyncio.to_thread(self.sync_node.exec_fallback, prep_res, exc)


class ReturnDefaultActionNode(Node):
    def post(self, shared, prep_res, exec_res):
        # This node simply returns the "default" action to the parent flow
        return "default" 