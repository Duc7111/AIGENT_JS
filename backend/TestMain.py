from Main import *
from pathlib import Path

# Get current working parent path
parent_path = Path(__file__).resolve().parents[1]

add_module('fileReader', 'IO', 'FileReader')
set_module_hyperparameters(key='fileReader', hyperparameters={'file': 'backend\\Test.read.txt'})
output_register(key='output', srcModuleKey='fileReader', srcKey='output')

add_module('textHolder', 'IO', 'TextHolder')
set_module_hyperparameters(key='textHolder', hyperparameters={'text': 'Hello World!'})

add_module('fileWriter', 'IO', 'FileWriter')
set_module_hyperparameters(key='fileWriter', hyperparameters={'file': 'backend\\Test.write.txt'})

connect_modules('textHolder', 'fileWriter', 'output', 'input')

res = run()
if res['status']:
    print(res['outputs'])
else: 
    print(res['msg'])

# Save pipeline to file
save_pipeline(parent_path / '__cache__' / 'TestMain.json')
