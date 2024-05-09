
from Main import *
from pathlib import Path

is_run = False

parent_path = Path(__file__).resolve().parents[1]

add_module('pipeline', 'HuggingFace', 'Pipeline')
set_module_hyperparameters('pipeline', {'task': 'question-answering', 'model': 'deepset/tinyroberta-squad2', 'tokenizer': 'deepset/tinyroberta-squad2'})

add_module('dictMerger', 'Caster', 'DictMerger')
set_module_hyperparameters('dictMerger', {'keys': ['question', 'context']})

connect_modules('questionHolder', 'dictMerger', 'output', 'question')
connect_modules('contextHolder', 'dictMerger', 'output', 'context')

connect_modules('dictMerger', 'pipeline', 'output', 'input')

input_register('question', 'dictMerger', 'question')
input_register('context', 'dictMerger', 'context')
output_register('output', 'pipeline', 'output')

if is_run:
    res = run()
    if res['status']:
        print(res['outputs'])
    else:
        print(res['msg'])

save_pipeline(parent_path / '__cache__' / 'TestHuggingFace.json')

