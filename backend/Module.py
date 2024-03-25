
from threading import *

from Container import Buffer

class Module:

    inputBuffer: dict[str, Buffer | None]
    outputBuffer: dict[str, Buffer]
    input: dict[str, any]
    hyperparameters: dict[str, any]
    status: bool

    def __init__(self) -> None:
        self.inputBuffer = dict()
        self.outputBuffer = dict()
        self.input = dict()
        self.hyperparameters = dict()
        self.status = True
    
    def run(self) -> None:
        for key in self.inputBuffer:
            if self.inputBuffer[key] is None:
                continue
            self.input[key] = self.inputBuffer[key].get_val(id(self))
            if self.input[key] is None:
                self.status = False
                return
        self.status = True
 
class Pipeline(Module):
    
    modules: dict[str, Module]
    threads: dict[str, Thread]

    def __init__(self):
        self._modules = dict()
        self.threads = dict()

    def run(self) -> None:
        for key in self.modules:
            self.threads[key].start()
        for key in self.modules:
            self.threads[key].join()
        for key in self.modules:
            if not self.modules[key].status:
                self.status = False
                return

    def add_module(self, key: str, module: Module) -> bool:
        if key in self.modules:
            return False
        self.modules[key] = module
        self.threads[key] = Thread(target = self.modules[key].run)
        return True
    
    def remove_module(self, key: str) -> bool:
        if key in self.modules:
            del self.modules[key]
            del self.threads[key]
            return True
        return False
        
    def connect(self, srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> bool:
        if srcModuleKey not in self.modules or tgtModuleKey not in self.modules:
            return False
        if srcKey not in self.modules[srcModuleKey].outputBuffer or tgtKey not in self.modules[tgtModuleKey].inputBuffer:
            return False
        self.modules[srcModuleKey].outputBuffer[srcKey].register(id(self.modules[tgtModuleKey]))
        self.modules[tgtModuleKey].inputBuffer[tgtKey] = self.modules[srcModuleKey].outputBuffer[srcKey]
        return True
        
    def disconnect(self, srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> bool:
        if srcModuleKey not in self.modules or tgtModuleKey not in self.modules:
            return False
        if srcKey not in self.modules[srcModuleKey].outputBuffer or tgtKey not in self.modules[tgtModuleKey].inputBuffer:
            return False
        self.modules[srcModuleKey].outputBuffer[srcKey].unregister(id(self.modules[tgtModuleKey]))
        self.modules[tgtModuleKey].inputBuffer[tgtKey] = None
        return True
        
    