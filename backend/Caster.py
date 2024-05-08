
from Module import Module
from Container import Buffer

class DictSplitter(Module):

    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('keys')
        self.hyperparameters['keys'] = []
        self.inputBuffer['input'] = None
    
    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            for key in self.hyperparameters['keys']:
                self.outputBuffer[key].set_val(self.input['input'][key])
            self.status = True
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in DictSplitter")
            return
        
    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters): 
            return False
        self.outputBuffer = dict() # clear outputBuffer
        for key in hyperparameters['keys']:
            self.outputBuffer[key] = Buffer(None)
        self.changed = True
        return True

class DictMerger(Module):

    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('keys')
        self.hyperparameters['keys'] = []
        self.outputBuffer['output'] = Buffer(None)
        self.inputBuffer['input'] = None
    
    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = {key: self.input[key] for key in self.hyperparameters['keys']}
            self.outputBuffer['output'].set_val(res)
            self.status = True
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in DictMerger")
            return
        
    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters): 
            return False
        self.inputBuffer = dict() # clear inputBuffer
        for key in hyperparameters['keys']:
            self.inputBuffer[key] = None
        self.changed = True
        return True
    
class ArraySplitter(Module):

    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('index')
        self.hyperparameters['index'] = []
        self.inputBuffer['input'] = None
    
    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            for i in self.hyperparameters['index']:
                self.outputBuffer[str(i)].set_val(self.input['input'][i])
            self.status = True
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in ArraySplitter")
            return
        
    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters): 
            return False
        self.outputBuffer = dict() # clear outputBuffer
        for i in hyperparameters['index']:
            self.outputBuffer[str(i)] = Buffer(None)
        self.changed = True
        return True
    
class ArrayMerger(Module):
    
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('index')
        self.hyperparameters['index'] = []
        self.outputBuffer['output'] = Buffer(None)
        self.inputBuffer['input'] = None
    
    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = [self.input[i] for i in self.hyperparameters['index']]
            self.outputBuffer['output'].set_val(res)
            self.status = True
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in ArrayMerger")
            return
        
    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters): 
            return False
        self.inputBuffer = dict() # clear inputBuffer
        for i in hyperparameters['index']:
            self.inputBuffer[i] = None
        self.changed = True
        return True