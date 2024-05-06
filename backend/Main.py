
import socket
import json
from importlib import import_module

from Module import *

HOST = '127.0.0.1'
PORT = 7777

pipeline: Pipeline = Pipeline()

def load_pipeline(path: str) -> dict:
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except:
        return {'status': False, 'outputs': {}}
    pipeline.inputBuffer = dict()
    for key, val in data['inputBuffer']:
        pipeline.inputBuffer[key] = Buffer(val)
    pipeline.outputBuffer = dict()
    for key, val in data['outputBuffer']:
        pipeline.outputBuffer[key] = Buffer(val)
    for key, val in data['hyperparameters']:
        pipeline.hyperparameters[key] = val
    pipeline.hyperparameters_list = data['hyperparameters_list']
    pipeline.modules = dict()
    for key, val in data['modules']:
        res = add_module(key, **val)
        if not res['status']:
            return res
    for key in data['regDict']:
        key = key.split(',')
        res = connect_modules(*key)
        if not res['status']:
            return res
    return {'status': True, 'outputs': {}}

def save_pipeline(path: str) -> dict:
    data = dict()
    data['inputBuffer'] = {key: pipeline.inputBuffer[key]._val for key in pipeline.inputBuffer}
    data['outputBuffer'] = {key: pipeline.outputBuffer[key]._val for key in pipeline.outputBuffer}
    data['hyperparameters'] = pipeline.hyperparameters
    data['hyperparameters_list'] = pipeline.hyperparameters_list
    data['modules'] = {key: (type(val).__module__, type(val).__name__) for key, val in pipeline.modules.items()}
    data['regDict'] = {key: None for key in pipeline.regDict}
    try:
        with open(path, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        return {'status': False, 'message': str(e), 'outputs': {}}
    return {'status': True, 'outputs': {}}
                
def add_module(key: str, type: str, module: str) -> dict:
    type = import_module(type)
    module = getattr(type, module)
    module = module()
    return {
        'status': pipeline.add_module(key, module), 
        'outputs': {
            'hyperparameters': module.hyperparameters_list,
            'inputs': module.inputBuffer.keys(),
            'outputs': module.outputBuffer.keys()
        }
        }

def remove_module(key: str) -> dict:
    return {
        'status': pipeline.remove_module(key), 
        'outputs': {}
        }

def set_module_hyperparameters(key: str, hyperparameters: dict) -> dict:
    module = pipeline.modules[key]
    status = module.set_hyperparameters(hyperparameters)
    outputs = {
        'hyperparameters': pipeline.modules[key].hyperparameters_list,
        'inputs': module.inputBuffer.keys(),
        'outputs': module.outputBuffer.keys()
        } if pipeline.changed else {}
    pipeline.changed = False
    return {
        'status': status,
        'outputs': outputs
        }

def connect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    print(srcModuleKey, tgtModuleKey, srcKey, tgtKey)
    return {
        'status': pipeline.connect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {}
        }

def disconnect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {}
        }

def input_register(key: str, tgtModuleKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.input_register(key, tgtModuleKey, tgtKey), 
        'outputs': {}
        }

def input_unregister(key: str) -> dict:
    return {
        'status': pipeline.input_unregister(key), 
        'outputs': {}
        }

def output_register(key: str, srcModuleKey: str, srcKey: str) -> dict:
    return {
        'status': pipeline.output_register(key, srcModuleKey, srcKey), 
        'outputs': {}
        }

def output_unregister(key: str) -> dict:
    return {
        'status': pipeline.output_unregister(key), 
        'outputs': {}
        }
    
def run() -> dict:
    pipeline.run()
    return {
        'status': pipeline.status, 
        'outputs': {
            key: pipeline.outputBuffer[key]._val for key in pipeline.outputBuffer
            }
        }


request = globals()

if __name__ == '__main__':
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
                conn.sendall(json.dumps(res).encode())
