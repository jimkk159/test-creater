import os
from utils.utils import copy_file
from myPocketFlow import Node
from config import SharedKeys

class CopyFileNode(Node):
    def __init__(self, dir_path, suffix="_copy", is_use_function_name=False):
        super().__init__()
        self.dir_path = dir_path
        self.suffix = suffix
        self.is_use_function_name = is_use_function_name

    def prep(self, shared):
        function_name = ''
        if self.is_use_function_name:
            function_name = self.params[SharedKeys.FUNCTION_NAME] + '_'

        self.source = shared[SharedKeys.FILE_PATH]
        base_name = os.path.basename(self.source)
        name, ext = os.path.splitext(base_name)
        self.file_name = f"{function_name}{name}{self.suffix}{ext}"

    def exec(self, _):
        self.destination = copy_file(self.source, self.file_name)

    def post(self, shared, prep_res, exec_res):
        if SharedKeys.SUGGESTED_FILE_PATH not in shared:
            shared[SharedKeys.SUGGESTED_FILE_PATH] = {}
            
        if self.is_use_function_name:
            function_name = self.params[SharedKeys.FUNCTION_NAME]
            shared[SharedKeys.SUGGESTED_FILE_PATH][function_name] = os.path.abspath(self.destination)
        else:
            shared[SharedKeys.SUGGESTED_FILE_PATH] = os.path.abspath(self.destination)