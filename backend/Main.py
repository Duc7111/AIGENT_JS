
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
    
    # Clear pipeline
    pipeline.modules = {}
    pipeline.regDict = {}
    pipeline.inputBuffer = {}
    pipeline.outputBuffer = {}
    pipeline.hyperparameters = {}
    pipeline.hyperparameters_list = []

    for key, val in data['inputBuffer'].items():
        pipeline.inputBuffer[key] = Buffer(val)

    for key, val in data['outputBuffer'].items():
        pipeline.outputBuffer[key] = Buffer(val)
    
    for key, val in data['hyperparameters'].items():
        pipeline.hyperparameters[key] = val

    pipeline.hyperparameters_list = data['hyperparameters_list']

    for key, val in data['modules'].items():
        res = add_module(key, val['type'], val['module'])
        if not res['status']:
            return res
        res = set_module_hyperparameters(key, val['hyperparameters'])
        if not res['status']:
            return res

    for key in data['regDict']:
        parsed_key = tuple(map(str, key.split(', ')))
        if len(parsed_key) == 4:
            res = connect_modules(*parsed_key)
            if not res['status']:
                return res
        elif len(parsed_key) == 2:
            if parsed_key[0] == 'True':
                res = input_register(parsed_key[1], *data['regDict'][key])
            else:
                res = output_register(parsed_key[1], *data['regDict'][key])
            if not res['status']:
                return res  
    return {'status': True, 'outputs': {}}

def __tuple_to_str(t: tuple) -> str:
    return ', '.join(map(str, t))

def save_pipeline(path: str) -> dict:
    data = dict()
    data['inputBuffer'] = {key: pipeline.inputBuffer[key]._val for key in pipeline.inputBuffer}
    data['outputBuffer'] = {key: pipeline.outputBuffer[key]._val for key in pipeline.outputBuffer}
    data['hyperparameters'] = pipeline.hyperparameters
    data['hyperparameters_list'] = pipeline.hyperparameters_list
    data['modules'] = {key: {'type': type(val).__module__, 'module': type(val).__name__, 'hyperparameters': val.hyperparameters} for key, val in pipeline.modules.items()}
    data['regDict'] = {__tuple_to_str(key): val for key, val in pipeline.regDict.items()}
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
    if pipeline.changed:
        outputs = {
            'hyperparameters': pipeline.modules[key].hyperparameters_list,
            'inputs': module.inputBuffer.keys(),
            'outputs': module.outputBuffer.keys()
            }
        pipeline.full_disconnect(key)
        pipeline.changed = False
    else:
        outputs = {}
    return {
        'status': status,
        'outputs': outputs
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
