
from threading import *

from Container import Buffer

class Module:

    inputBuffer: dict[str, Buffer | None]
    outputBuffer: dict[str, Buffer]
    input: dict[str, any]
    hyperparameters: dict[str, any]
    hyperparameters_list: tuple[str]
    status: bool

    def __init__(self) -> None:
        self.inputBuffer = dict()
        self.outputBuffer = dict()
        self.input = dict()
        self.hyperparameters = dict()
        self.hyperparameters_list = tuple()
        self.status = True
    
    # Check if all inputs are available, call by child class run method
    def run(self) -> None:
        for key in self.inputBuffer:
            if self.inputBuffer[key] is None:
                continue
            self.input[key] = self.inputBuffer[key].get_val(id(self))
            if self.input[key] is None:
                self.status = False
                return
        self.status = True

    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> None:
        self.hyperparameters = dict()
        for key in hyperparameters:
            if key in self.hyperparameters_list:
                self.hyperparameters[key] = hyperparameters[key]
 
class Pipeline(Module):
    
    modules: dict[str, Module]
    threads: dict[str, Thread]
    regDict: dict[tuple[str, str, str, str], None]
    
    def __init__(self):
        super().__init__()
        self.modules = dict()
        self.threads = dict()
        self.regDict = dict()

    def run(self) -> None:
        super().run()
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
            # Disconnect all connections
            for (srcModuleKey, tgtModuleKey, srcKey, tgtKey) in list(self.regDict.keys()):
                if srcModuleKey == key or tgtModuleKey == key:
                    self.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey)
                    del self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)]
            del self.modules[key]
            del self.threads[key]
            return True
        return False
        
    def connect(self, srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> bool:
        if srcModuleKey not in self.modules or tgtModuleKey not in self.modules:
            return False
        if srcKey not in self.modules[srcModuleKey].outputBuffer or tgtKey not in self.modules[tgtModuleKey].inputBuffer:
            return False
        if (srcModuleKey, tgtModuleKey, srcKey, tgtKey) not in self.regDict:
            self.modules[srcModuleKey].outputBuffer[srcKey].register(id(self.modules[tgtModuleKey]))
            self.modules[tgtModuleKey].inputBuffer[tgtKey] = self.modules[srcModuleKey].outputBuffer[srcKey]
            self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)] = None
        return True
        
    def disconnect(self, srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> bool:
        if srcModuleKey not in self.modules or tgtModuleKey not in self.modules:
            return False
        if srcKey not in self.modules[srcModuleKey].outputBuffer or tgtKey not in self.modules[tgtModuleKey].inputBuffer:
            return False
        if (srcModuleKey, tgtModuleKey, srcKey, tgtKey) in self.regDict:
            self.modules[srcModuleKey].outputBuffer[srcKey].unregister(id(self.modules[tgtModuleKey]))
            self.modules[tgtModuleKey].inputBuffer[tgtKey] = None
            del self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)]
        return True
    

    