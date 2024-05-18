
import socket
import json
from importlib import import_module

from Module import *

HOST = '127.0.0.1'
PORT = 7777

pipeline: Pipeline = Pipeline()

def __tuple_to_str(t: tuple) -> str:
    return ', '.join(map(str, t))

def __json_to_pipeline(json: dict) -> Pipeline:
    resPipeline = Pipeline()
    resPipeline.hyperparameters_list = json['hyperparameters_list']
    resPipeline.hyperparameters = json['hyperparameters']
    resPipeline.modules = {}
    for key, val in json['modules'].items():
        if 'type' not in val:
            resPipeline.modules[key] = __json_to_pipeline(val)
        else:
            type = import_module(val['type'])
            module = getattr(type, val['module'])
            module: Module = module()
            module.set_hyperparameters(val['hyperparameters'])
            resPipeline.add_module(key, module)
    for key, val in json['regDict'].items():
        parsed_key = tuple(map(str, key.split(', ')))
        if len(parsed_key) == 2:
            if parsed_key[0] == 'True':
                resPipeline.input_register(parsed_key[1], val[0], val[1])
            else:
                resPipeline.output_register(parsed_key[1], val[0], val[1])
        else:
            resPipeline.connect(parsed_key[0], parsed_key[1], parsed_key[2], parsed_key[3])
    return resPipeline

def __pipeline_to_json(pipeline: Pipeline) -> dict:
    data = dict()
    data['inputBuffer'] = {key: pipeline.inputBuffer[key].get_val(0) for key in pipeline.inputBuffer}
    data['outputBuffer'] = {key: pipeline.outputBuffer[key].get_val(0) for key in pipeline.outputBuffer}
    data['hyperparameters'] = pipeline.hyperparameters
    data['hyperparameters_list'] = pipeline.hyperparameters_list
    data['modules'] = {}
    for key, val in pipeline.modules.items():
        if val.__class__.__module__ == 'Module' and val.__class__.__name__ == 'Pipeline':
            data['modules'][key] = __pipeline_to_json(val)
        else:
            data['modules'][key] = {
                'type': val.__class__.__module__,
                'module': val.__class__.__name__,
                'hyperparameters': val.hyperparameters,
            }
    data['regDict'] = {__tuple_to_str(key): val for key, val in pipeline.regDict.items()}
    return data

def load_pipeline(path: str) -> dict:
    try:
        global pipeline
        with open(path, 'r') as f:
            pipeline = __json_to_pipeline(json.load(f))
    except Exception as e:
        return {'status': False, 'outputs': {}, 'msg': str(e)}
    return {'status': True, 'outputs': {}, 'msg': None}
    
def load_pipeline_as_module(key: str, path: str) -> dict:
    try:
        with open(path, 'r') as f:
            res = __json_to_pipeline(json.load(f))
    except Exception as e:
        return {'status': False, 'outputs': {}, 'msg': str(e)}
    return {
        'status': pipeline.add_module(key, res), 
        'outputs': {
            'hyperparameters': res.hyperparameters_list,
            'inputs': list(res.inputBuffer.keys()), 
            'outputs': list(res.outputBuffer.keys())
        }, 
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def save_pipeline(path: str) -> dict:
    try:
        data = __pipeline_to_json(pipeline)
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
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def remove_module(key: str) -> dict:
    return {
        'status': pipeline.remove_module(key), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg'].get_val(0)
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
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def connect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.connect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def disconnect_modules(srcModuleKey: str, tgtModuleKey: str, srcKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.disconnect(srcModuleKey, tgtModuleKey, srcKey, tgtKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def input_register(key: str, tgtModuleKey: str, tgtKey: str) -> dict:
    return {
        'status': pipeline.input_register(key, tgtModuleKey, tgtKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def input_unregister(key: str) -> dict:
    return {
        'status': pipeline.input_unregister(key), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def output_register(key: str, srcModuleKey: str, srcKey: str) -> dict:
    return {
        'status': pipeline.output_register(key, srcModuleKey, srcKey), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def output_unregister(key: str) -> dict:
    return {
        'status': pipeline.output_unregister(key), 
        'outputs': {},
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }
    
def run() -> dict:
    pipeline.run()
    outputs = {}
    for key in pipeline.outputBuffer:
        if key != 'msg':
            outputs[key] = pipeline.outputBuffer[key].get_val(0)
    return {
        'status': pipeline.status, 
        'outputs': outputs,
        'msg': pipeline.outputBuffer['msg'].get_val(0)
        }

def reset() -> dict:
    global pipeline
    pipeline = Pipeline()
    return {'status': True, 'outputs': {}, 'msg': None}

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
                print(data)
                res = request[data['request']](**data['inputs'])
                conn.sendall(json.dumps(res).encode())
                pipeline.outputBuffer['msg']._val = None
