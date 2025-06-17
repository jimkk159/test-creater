import os
import shutil
from myPocketFlow import Node

class CopyFileNode(Node):
    def __init__(self, dir_path, prefix="", suffix="_copy"):
        super().__init__()
        self.dir_path = dir_path
        self.suffix = suffix
        self.prefix = prefix

    def prep(self, shared):
        self.source = shared["file_path"]
        base_name = os.path.basename(self.source)
        name, ext = os.path.splitext(base_name)
        self.file_name = f"{self.prefix}{name}{self.suffix}{ext}"
        self.destination = os.path.join(self.dir_path, self.file_name)

    def exec(self, _):
        shutil.copyfile(self.source, self.destination)

    def post(self, shared, prep_res, exec_res):
        shared["file_path"] = os.path.abspath(self.destination)