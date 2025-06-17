import os
import shutil
from myPocketFlow import Node

class CopyFileNode(Node):
    def __init__(self, destination, prefix="", suffix="_copy"):
        super().__init__()
        self.destination = destination
        self.suffix = suffix
        self.prefix = prefix

    def prep(self, shared):
        self.source = shared["file_path"]

    def exec(self, _):
        base_name = os.path.basename(self.source)
        name, ext = os.path.splitext(base_name)
        file_name = f"{self.prefix}{name}{self.suffix}{ext}"
        shutil.copyfile(self.source, os.path.join(self.destination, file_name))

    def post(self, shared, prep_res, exec_res):
        shared["file_path"] = os.path.abspath(self.destination)