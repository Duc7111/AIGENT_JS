
import os
import socket

import json

import HuggingFace as hf
import Module

HOST = '127.0.0.1'
PORT = 7777

modules = dict()

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("Starting server")
        s.bind((HOST, PORT))
        print("Connected to server")
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data = json.loads(data)
                match data['command']:
                    case 'create':
                        match data['object_type']:
                            case 'model':
                                if data['object_name'] in modules:
                                    print('Object already exists')
                                else:
                                    modules[data['object_name']] = hf.Model(data['name'])
                                    print('Object created')
                                    
                            case 'tokenizer':
                                if data['object_name'] in modules:
                                    print('Object already exists')
                                else:
                                    modules[data['object_name']] = hf.Tokenizer(data['name'])
                                    print(b'Object created')
                                    
                            case 'hf_pipeline':
                                if data['object_name'] in modules:
                                    print('Object already exists')
                                else:
                                    inputs = data['inputs']
                                    modules[data['object_name']] = hf.Pipeline(**inputs)
                                    print('Object created')
                                    
                    case 'run':
                        if data['object_name'] in modules:
                            conn.sendall(json.dumps(modules[data['object_name']].run(data['inputs'])).encode())
                        else:
                            print('Object does not exist')
                            
                    case _:
                        print('Invalid command')
                