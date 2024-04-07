
import os
import socket
import json
from importlib import import_module

from Module import *

HOST = '127.0.0.1'
PORT = 7777

pipeline: Pipeline = Pipeline()

if __name__ == '__main__':
    request = globals()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Starting server")
        s.bind((HOST, PORT))
        print("Connected to host")
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = json.loads(data)
                res = request[data['request']](**data['inputs'])
                conn.sendall(json.dumps(res.__dict__).encode())



def load_pipeline(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except:
        return {'status': False, 'outputs': {}}
    for key in data:
        add_module(key, **data[key])
    return {'status': True, 'outputs': {}}

def save_pipeline(path: str) -> dict:
    data = dict()
    for key in pipeline.modules:
        data[key] = (pipeline.modules[key].__class__.__module__, pipeline.modules[key].__class__.__name__)
    try:
        with open(path, 'w') as f:
            json.dump(data, f)
    except:
        return {'status': False, 'outputs': {}}
    return {'status': True, 'outputs': {}}
                
def add_module(key: str, type: str, module: str) -> dict:
    type = import_module(type)
    module = getattr(type, module)
    return {
        'status': pipeline.add_module(key, module), 
        'outputs': {}
        }

def remove_module(key: str) -> dict:
    return {
        'status': pipeline.remove_module(key), 
        'outputs': {}
        }

def set_module_hyperparameters(key: str, hyperparameters: dict) -> dict:
    return {
        'status': pipeline.modules[key].set_hyperparameters(hyperparameters),
        'outputs': {}
        }

def connect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.connect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {}
        }

def disconnect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {}
        }
    
def run() -> dict:
    pipeline.run()
    return {'status': pipeline.status, 'outputs': {key: pipeline.outputBuffer[key]._val for key in pipeline.outputBuffer}}
