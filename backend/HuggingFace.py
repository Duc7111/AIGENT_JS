import token
import torch
from transformers import Pipeline, pipeline, AutoTokenizer, AutoModel

from Module import Module
from Container import Buffer

class Model(Module):
    
    __model: AutoModel | None
    
    def __init__(self):
        super().__init__()
        self.__model = None
        self.hyperparameters_list = AutoModel.from_pretrained.__code__.co_varnames
        self.outputBuffer['output'] = Buffer('')
        self.inputBuffer['input'] = None
    
    def run(self) -> None:
        self.__model = AutoModel.from_pretrained(**self.hyperparameters)
        if self.__model is None:
            self.status = False
            return
        super().run()
        if self.status == False:
            return
        try:
            res = self.__model(**self.input)
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))
        
class Tokenizer(Module):
    
    __tokenizer: AutoTokenizer | None
        
    def __init__(self):
        super().__init__()
        self.__tokenizer = None
        self.hyperparameters_list = AutoTokenizer.from_pretrained.__code__.co_varnames
        self.outputBuffer['output'] = Buffer('')
        self.inputBuffer['input'] = None
        
    def run(self) -> None:
        self.__tokenizer = AutoTokenizer.from_pretrained(**self.hyperparameters)
        if self.__tokenizer is None:
            self.status = False
            return
        super().run()
        if self.status == False:
            return
        try:
            res = self.__tokenizer(**self.input)
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))

class Pipeline(Module):
    
    ___pipeline: Pipeline
    
    def __init__(self):
        super().__init__()
        self.___pipeline = None
        self.hyperparameters_list = pipeline.__code__.co_varnames
        self.outputBuffer['output'] = Buffer('')
        self.inputBuffer['input'] = None
    
    def run(self) -> None:
        self.___pipeline = pipeline(**self.hyperparameters)
        if self.___pipeline is None:
            self.status = False
            return
        super().run()
        if self.status == False:
            self.outputBuffer['output'].set_val(None)
            return
        try:
            res = self.___pipeline(**self.input['input'])
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))