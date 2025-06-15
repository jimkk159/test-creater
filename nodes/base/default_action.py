from myPocketFlow import Node

class ReturnDefaultActionNode(Node):
    def post(self, shared, prep_res, exec_res):
        # This node simply returns the "default" action to the parent flow
        return "default" 