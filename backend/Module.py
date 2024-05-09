
from threading import *

from Container import Buffer

class Module:

    inputBuffer: dict[str, Buffer | None]
    outputBuffer: dict[str, Buffer]
    input: dict[str, any]
    hyperparameters: dict[str, any]
    hyperparameters_list: tuple[str]
    status: bool
    changed: bool

    def __init__(self) -> None:
        self.inputBuffer = dict()
        self.outputBuffer = dict()
        self.outputBuffer['msg'] = Buffer(None)
        self.input = dict()
        self.hyperparameters = dict()
        self.hyperparameters_list = tuple()
        self.status = True
        self.changed = False
    
    # Check if all inputs are available, call by child class run method
    def run(self) -> None:
        self.status = True
        for key in self.inputBuffer:
            if self.inputBuffer[key] is None:
                continue
            self.input[key] = self.inputBuffer[key].get_val(id(self))
            if self.input[key] is None:
                self.status = False
                self.outputBuffer['msg'].set_val("Input " + str(key) + " is not available")
                return

    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        for key in hyperparameters:
            if key not in self.hyperparameters_list:
                return False
        for key in hyperparameters:
            self.hyperparameters[key] = hyperparameters[key]
        return True
 
class Pipeline(Module):
    
    modules: dict[str, Module]
    regDict: dict[tuple[str, str, str, str], None]
    input: dict[str, Buffer]

    def __init__(self):
        super().__init__()
        self.modules = dict()
        self.regDict = dict()

    def run(self) -> None:
        self.status = True
        for key in self.inputBuffer:
            if self.inputBuffer[key] is None:
                continue
            self.input[key].set_val(self.inputBuffer[key].get_val(id(self)))
            if self.input[key] is None:
                self.status = False
                self.outputBuffer['msg'].set_val("Input " + str(key) + " is not available")
                return
        threads: dict[str, Thread] = dict()
        try:
            for key in self.modules:
                threads[key] = Thread(target=self.modules[key].run)
                threads[key].start()
            for key in self.modules:
                threads[key].join()
            for key in self.modules:
                if not self.modules[key].status:
                    self.status = False
                    self.outputBuffer['msg'].set_val("Error in " + key + ": " + self.modules[key].outputBuffer['msg'].get_val(0))
                    return
        except Exception as e:
            self.status = False
            self.outputBuffer['msg'].set_val(str(e))
            return

    def add_module(self, key: str, module: Module) -> bool:
        if key in self.modules:
            return False
        self.modules[key] = module
        return True
    
    def remove_module(self, key: str) -> bool:
        if key in self.modules:
            # Disconnect all connections
            for (srcModuleKey, tgtModuleKey, srcKey, tgtKey) in list(self.regDict.keys()):
                if srcModuleKey == key or tgtModuleKey == key:
                    self.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey)
                    del self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)]
            del self.modules[key]
            return True
        return False
        
    def connect(self, srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> bool:
        if srcModuleKey not in self.modules or tgtModuleKey not in self.modules:
            return False
        if srcKey not in self.modules[srcModuleKey].outputBuffer or tgtKey not in self.modules[tgtModuleKey].inputBuffer:
            return False
        if (srcModuleKey, tgtModuleKey, srcKey, tgtKey) not in self.regDict:
            self.modules[srcModuleKey].outputBuffer[srcKey].register(id(self.modules[tgtModuleKey].inputBuffer[tgtKey]))
            self.modules[tgtModuleKey].inputBuffer[tgtKey] = self.modules[srcModuleKey].outputBuffer[srcKey]
            self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)] = None
        return True
        
    def disconnect(self, srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> bool:
        if srcModuleKey not in self.modules or tgtModuleKey not in self.modules:
            return False
        if srcKey not in self.modules[srcModuleKey].outputBuffer or tgtKey not in self.modules[tgtModuleKey].inputBuffer:
            return False
        if (srcModuleKey, tgtModuleKey, srcKey, tgtKey) in self.regDict:
            self.modules[srcModuleKey].outputBuffer[srcKey].unregister(id(self.modules[tgtModuleKey].inputBuffer[tgtKey]))
            self.modules[tgtModuleKey].inputBuffer[tgtKey] = None
            del self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)]
        return True
    
    def full_disconnect(self, key: str = None) -> None:
        if key is not None:
            for (srcModuleKey, tgtModuleKey, srcKey, tgtKey) in list(self.regDict.keys()):
                if srcModuleKey == key or tgtModuleKey == key:
                    self.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey)
                    del self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)]
            for (type, key) in list(self.regDict.keys()):
                if self.regDict[(type, key)][0] == key or self.regDict[(type, key)][1] == key:
                    if type: self.input_unregister(key)
                    else: self.output_unregister(key)
        else:
            for (srcModuleKey, tgtModuleKey, srcKey, tgtKey) in list(self.regDict.keys()):
                self.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey)
                del self.regDict[(srcModuleKey, tgtModuleKey, srcKey, tgtKey)]
            for (type, key) in list(self.regDict.keys()):
                if type: self.input_unregister(key)
                else: self.output_unregister(key)
    
    def input_register(self, key: str, tgtModelKey: str, tgtKey: str) -> bool:
        if tgtModelKey not in self.modules or tgtKey not in self.modules[tgtModelKey].inputBuffer:
            return False
        if key not in self.inputBuffer:
            self.inputBuffer[key] = None
        if key not in self.input:
            self.input[key]= Buffer(None)
        self.input[key].register(id(self.modules[tgtModelKey].inputBuffer[tgtKey]))
        self.modules[tgtModelKey].inputBuffer[tgtKey] = self.input[key]
        self.regDict[(True, key)] = [tgtModelKey, tgtKey]   
        return True
    
    def input_unregister(self, key: str) -> bool:
        if key not in self.inputBuffer:
            return False
        if (True, key) in self.regDict:
            tgtModelKey, tgtKey = self.regDict[(True, key)]
            self.inputBuffer[key].unregister(id(self.modules[tgtModelKey].inputBuffer[tgtKey]))
            self.modules[tgtModelKey].inputBuffer[tgtKey] = None
            del self.inputBuffer[key]
            del self.regDict[(True, key)]
        return True
        
    def output_register(self, key: str, srcModelKey: str, srcKey: str) -> bool:
        if srcModelKey not in self.modules or srcKey not in self.modules[srcModelKey].outputBuffer:
            return False
        if key not in self.outputBuffer:
            self.outputBuffer[key] = Buffer(None)
        self.modules[srcModelKey].outputBuffer[srcKey].register(id(self.outputBuffer[key]))
        self.outputBuffer[key] = self.modules[srcModelKey].outputBuffer[srcKey]
        self.regDict[(False, key)] = [srcModelKey, srcKey]
        return True
    
    def output_unregister(self, key: str) -> bool:
        if key not in self.outputBuffer:
            return False
        if (False, key) in self.regDict:
            srcModelKey, srcKey = self.regDict[(False, key)]
            self.modules[srcModelKey].outputBuffer[srcKey].unregister(id(self.outputBuffer[key]))
            del self.outputBuffer[key]
            del self.regDict[(False, key)]
        return True
