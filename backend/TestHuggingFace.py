
from Main import *
from pathlib import Path

parent_path = Path(__file__).resolve().parents[1]

add_module('pipeline', 'HuggingFace', 'Pipeline')
set_module_hyperparameters('pipeline', {'task': 'question-answering', 'model': 'deepset/tinyroberta-squad2', 'tokenizer': 'deepset/tinyroberta-squad2'})

add_module('questionHolder', 'IO', 'TextHolder')
set_module_hyperparameters('questionHolder', {'text': 'What is the task?'})

add_module('contextHolder', 'IO', 'TextHolder')
set_module_hyperparameters('contextHolder', {'text': 'The task is to answer questions.'})

add_module('dictMerger', 'Caster', 'DictMerger')
set_module_hyperparameters('dictMerger', {'keys': ['question', 'context']})

connect_modules('questionHolder', 'dictMerger', 'output', 'question')
connect_modules('contextHolder', 'dictMerger', 'output', 'context')

connect_modules('dictMerger', 'pipeline', 'output', 'input')

output_register('output', 'pipeline', 'output')

res = run()
if res['status']:
    print(res['outputs'])
else:
    print(res['msg'])

save_pipeline(parent_path / '__cache__' / 'TestHuggingFace.json')

