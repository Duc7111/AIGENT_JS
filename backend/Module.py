
import string
from tkinter import SEL


class Module:
    
    def run(self, inputs: dict) -> dict:
        return dict()
        
    def modify(self, stats: dict) -> bool:
        return False
 
class Pipeline(Module):
    
    modules: list

    def __init__(self):
        self.modules = []
        self.ioMap = dict()
     
    def addModule(self, module: Module):
        self.modules.append(module)