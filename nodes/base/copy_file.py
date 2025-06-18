import os
from utils.utils import copy_file
from myPocketFlow import Node
from config import SharedKeys

class CopyFileNode(Node):
    def __init__(self, dir_path, suffix="_copy"):
        super().__init__()
        self.dir_path = dir_path
        self.suffix = suffix

    def prep(self, shared):
        self.source = shared[SharedKeys.FILE_PATH]
        base_name = os.path.basename(self.source)
        name, ext = os.path.splitext(base_name)
        self.file_name = f"{name}{self.suffix}{ext}"

    def exec(self, _):
        self.destination = copy_file(self.source, self.file_name)

    def post(self, shared, prep_res, exec_res):
        shared[SharedKeys.SUGGESTED_FILE_PATH] = os.path.abspath(self.destination)