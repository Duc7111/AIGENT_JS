import token
import torch
from transformers import Pipeline, pipeline, AutoTokenizer, AutoModel

from Module import Module

class Model(Module):
    
    model: AutoModel
    
    def __init__(self, name: str):
        self.model = AutoModel.from_pretrained(name)
    
    def run(self, inputs: dict) -> dict:
        return self.model(**inputs)

class Tokenizer(Module):
    
    tokenizer: AutoTokenizer
        
    def __init__(self, name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(name)
        
    def run(self, inputs: dict) -> dict:
        return self.tokenizer(**inputs)

class Pipeline(Module):
    
    nlp: Pipeline
    
    def __init__(self, task: str, tokenizer_name: str, model_name: str):
        self.nlp = pipeline(task=task, model=model_name, tokenizer=tokenizer_name)
    
    def run(self, inputs: dict) -> dict:
        return self.nlp(**inputs)