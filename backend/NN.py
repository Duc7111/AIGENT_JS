
from typing import Callable

from Module import Module
from Container import Buffer
import Activation
import Normalizer

def _vectorDot(x: list[float], y: list[float]) -> float:
    res = 0
    for i in range(len(x)):
        res += x[i] * y[i]
    return res

def _matrixCross(x: list[list[float]], y: list[list[float]]) -> list[list[float]]:
    res: list[list[float]] = []
    for i in range(len(x)):
        res.append([])
        for j in range(len(y[0])):
            res[i].append(_vectorDot(x[i], [y[k][j] for k in range(len(y))]))
    return res

class Perceptron(Module):
    
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('weights', 'bias')
        self.hyperparameters['weights'] = None
        self.hyperparameters['bias'] = None
        self.outputBuffer['output'] = Buffer(0)
        self.inputBuffer['input'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = _vectorDot(self.hyperparameters['weights'], self.input['input']) + self.hyperparameters['bias']
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))
            
        
class NeuralUnit(Module):

    activation: Callable
    
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('weights', 'bias', 'activation')
        self.hyperparameters['weights'] = None
        self.hyperparameters['bias'] = None
        self.hyperparameters['activation'] = 'none'
        self.activation = Activation.none
        self.outputBuffer['output'] = Buffer(0)
        self.inputBuffer['input'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = self.activation(_vectorDot(self.hyperparameters['weights'], self.input['input']) + self.hyperparameters['bias'])
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))

    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters):
            return False
        try:
            self.activation = getattr(Activation, self.hyperparameters['activation'])
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Activation function not found")
            self.hyperparameters['activation'] = 'none'
            self.activation = Activation.none
            return False
        return True 
            
        
class InputLayer(Module):
    
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('input_shape')
        self.hyperparameters['input_shape'] = None
        self.outputBuffer['output'] = Buffer(None)
        self.inputBuffer['input'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = self.input['input']
            if len(res) != self.hyperparameters['input_shape']:
                self.status = False
                self.outputBuffer['output'].set_val(None)
                self.outputBuffer['msg'].set_val("Input shape mismatch")
                return
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))
            
        
class FullyConnectedHiddenLayer(Module):

    activation: Callable

    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('#unit', "#input", 'weights', 'activation')
        self.hyperparameters['#unit'] = 0
        self.hyperparameters['#input'] = 0
        self.hyperparameters['weights'] = None
        self.hyperparameters['activation'] = 'none'
        self.activation = Activation.none
        self.outputBuffer['output'] = Buffer(None)
        self.inputBuffer['input'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = []
            for i in range(self.hyperparameters['#unit']):
                res.append(self.hyperparameters['activation'](_vectorDot(self.hyperparameters['weights'][i], self.input['input'])))
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))
    
    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters):
            return False
        try:
            self.activation = getattr(Activation, self.hyperparameters['activation'])
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Activation function not found")
            self.hyperparameters['activation'] = 'none'
            self.activation = Activation.none
            return False
        return True

class OutputLayer(Module):

    normalizer: Callable

    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('#unit', "#input", 'weights', 'normailizer')
        self.hyperparameters['#unit'] = 0
        self.hyperparameters['#input'] = 0
        self.hyperparameters['weights'] = None
        self.hyperparameters['normailizer'] = 'none'
        self.normalizer = Normalizer.none
        self.outputBuffer['output'] = Buffer(None)
        self.inputBuffer['input'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = []
            for i in range(self.hyperparameters['#unit']):
                res.append(_vectorDot(self.hyperparameters['weights'][i], self.input['input']))
            res = self.hyperparameters['normailizer'](res)
            self.outputBuffer['output'].set_val(res)
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))
        
    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters):
            return False
        try:
            self.normalizer = getattr(Normalizer, self.hyperparameters['normalizer'])
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Normalizer function not found")
            self.hyperparameters['normalizer'] = 'none'
            self.normalizer = Normalizer.none
            return False
        return True
        