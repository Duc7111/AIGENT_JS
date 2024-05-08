
from Main import *
from pathlib import Path


parent_path = Path(__file__).resolve().parents[1]

add_module('vectorHolder', 'IO', 'VectorHolder')
set_module_hyperparameters(key='vectorHolder', hyperparameters={'vector': [1, 0]})

add_module('perceptron', 'NN', 'Perceptron')
set_module_hyperparameters(key='perceptron', hyperparameters={'weights': [1, 1], 'bias': 0})

output_register(key='perceptron', srcModuleKey='perceptron', srcKey='output')
connect_modules('vectorHolder', 'perceptron', 'output', 'input')

# XOR gate using neural network
add_module('neuralUnit1', 'NN', 'NeuralUnit')
set_module_hyperparameters(key='neuralUnit1', hyperparameters={'weights': [1, 1], 'bias': 0, 'activation': 'ReLU'})

add_module('neuralUnit2', 'NN', 'NeuralUnit')
set_module_hyperparameters(key='neuralUnit2', hyperparameters={'weights': [1, 1], 'bias': -1, 'activation': 'ReLU'})

connect_modules('vectorHolder', 'neuralUnit1', 'output', 'input')
connect_modules('vectorHolder', 'neuralUnit2', 'output', 'input')

add_module('arrayMerger', 'Caster', 'ArrayMerger')
set_module_hyperparameters(key='arrayMerger', hyperparameters={'size': 2})

connect_modules('neuralUnit1', 'arrayMerger', 'output', '0')
connect_modules('neuralUnit2', 'arrayMerger', 'output', '1')

add_module('neuralUnit3', 'NN', 'NeuralUnit')
set_module_hyperparameters(key='neuralUnit3', hyperparameters={'weights': [1, -2], 'bias': 0, 'activation': 'ReLU'})

connect_modules('arrayMerger', 'neuralUnit3', 'output', 'input')
output_register(key='neuralUnit3', srcModuleKey='neuralUnit3', srcKey='output')

res = run()
if res['status']:
    print(res['outputs'])
else:
    print('error:' + res['outputs']['msg'])

save_pipeline(parent_path / '__cache__' / 'TestNN.json')