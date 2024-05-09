
import socket
import json
from importlib import import_module

from Module import *

HOST = '127.0.0.1'
PORT = 7777

pipeline: Pipeline = Pipeline()

def __json_to_pipeline(path: str) -> Pipeline:
    resPipeline = Pipeline()
    with open(path, 'r') as f:
        data = json.load(f)
    for key, val in data['inputBuffer'].items():
        resPipeline.inputBuffer[key] = Buffer(val)
    for key, val in data['outputBuffer'].items():
        resPipeline.outputBuffer[key] = Buffer(val) 
    for key, val in data['hyperparameters'].items():
        resPipeline.hyperparameters[key] = val
    resPipeline.hyperparameters_list = data['hyperparameters_list']
    for key, val in data['modules'].items():    
        res = add_module(key, val['type'], val['module'])
        if not res['status']:
            raise Exception (res['msg'])
        res = set_module_hyperparameters(key, val['hyperparameters'])
        if not res['status']:
            raise Exception (res['msg'])
    for key in data['regDict']:
        parsed_key = tuple(map(str, key.split(', ')))
        if len(parsed_key) == 4:
            res = connect_modules(*parsed_key)
            if not res['status']:
                raise Exception (res['msg'])
        elif len(parsed_key) == 2:
            if parsed_key[0] == 'True':
                res = input_register(parsed_key[1], *data['regDict'][key])
            else:
                res = output_register(parsed_key[1], *data['regDict'][key])
            if not res['status']:
                raise Exception (res['msg'])
    return resPipeline  

def load_pipeline(path: str) -> dict:
    try:
        global pipeline
        pipeline = __json_to_pipeline(path)
    except Exception as e:
        return {'status': False, 'outputs': {}, 'msg': str(e)}
    
def load_pipeline_as_module(key: str, path: str) -> dict:
    try:
        res = __json_to_pipeline(path)
    except Exception as e:
        return {'status': False, 'outputs': {}, 'msg': str(e)}
    return {
        'status': pipeline.add_module(key, res), 
        'outputs': {
            'hyperparameters': res.hyperparameters_list,
            'inputs': list(res.inputBuffer.keys()), 
            'outputs': list(res.outputBuffer.keys())
        }, 
        'msg': pipeline.outputBuffer['msg']._val
        }

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
        return {'status': False, 'outputs': {}, 'msg': str(e)}
    return {'status': True, 'outputs': {}, 'msg': None}
                
def add_module(key: str, type: str, module: str) -> dict:
    type = import_module(type)
    module = getattr(type, module)
    module: Module = module()
    return {
        'status': pipeline.add_module(key, module), 
        'outputs': {
            'hyperparameters': module.hyperparameters_list,
            'inputs': list(module.inputBuffer.keys()),
            'outputs': list(module.outputBuffer.keys())
        },
        'msg': pipeline.outputBuffer['msg']._val
        }

def remove_module(key: str) -> dict:
    return {
        'status': pipeline.remove_module(key), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg']._val
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
        'outputs': outputs,
        'msg': pipeline.outputBuffer['msg']._val
        }

def connect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.connect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg']._val
        }

def disconnect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg']._val
        }

def input_register(key: str, tgtModuleKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.input_register(key, tgtModuleKey, tgtKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg']._val
        }

def input_unregister(key: str) -> dict:
    return {
        'status': pipeline.input_unregister(key), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg']._val
        }

def output_register(key: str, srcModuleKey: str, srcKey: str) -> dict:
    return {
        'status': pipeline.output_register(key, srcModuleKey, srcKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg']._val
        }

def output_unregister(key: str) -> dict:
    return {
        'status': pipeline.output_unregister(key), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg']._val
        }
    
def run() -> dict:
    pipeline.run()
    outputs = {}
    for key in pipeline.outputBuffer:
        if key != 'msg':
            outputs[key] = pipeline.outputBuffer[key]._val
    return {
        'status': pipeline.status, 
        'outputs': outputs,
        'msg': pipeline.outputBuffer['msg']._val
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
                print(res)
                conn.sendall(json.dumps(res).encode())
