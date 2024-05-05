
from Module import Module

class Perceptron(Module):
    
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('weights', 'bias')
        self.hyperparameters['weights'] = None
        self.hyperparameters['bias'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = self.input['input'] @ self.hyperparameters['weights'] + self.hyperparameters['bias']
            self.outputBuffer['output'].set_val(res)
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in Perceptron")
            return
        
class NeuralUnit(Module):
    
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('weights', 'bias', 'activation')
        self.hyperparameters['weights'] = None
        self.hyperparameters['bias'] = None
        self.hyperparameters['activation'] = lambda x: x

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = self.hyperparameters['activation'](self.input['input'] @ self.hyperparameters['weights'] + self.hyperparameters['bias'])
            self.outputBuffer['output'].set_val(res)
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in NeuralUnit")
            return
        
class InputLayer(Module):
    
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('input_shape')
        self.hyperparameters['input_shape'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = self.input['input']
            if res.len() != self.hyperparameters['input_shape']:
                self.status = False
                self.outputBuffer['output'].set_val(None)
                self.outputBuffer['msg'].set_val("Input shape mismatch")
                return
            self.outputBuffer['output'].set_val(res)
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in FFInputLayer")
            return
        
class FullyConnectedHiddenLayer(Module):

    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('#unit', "#input", 'weights', 'activations')
        self.hyperparameters['#unit'] = 0
        self.hyperparameters['#input'] = 0
        self.hyperparameters['weights'] = None
        self.hyperparameters['activations'] = [] # list of activation functions

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = []
            for i in range(self.hyperparameters['#unit']):
                res.append(self.hyperparameters['activations'][i](self.input['input'] @ self.hyperparameters['weights'][i]))
            self.outputBuffer['output'].set_val(res)
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in FullyConnectedHiddenLayer")
            return

class OutputLayer(Module):

    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('#unit', "#input", 'weights', 'normailizer')
        self.hyperparameters['#unit'] = 0
        self.hyperparameters['#input'] = 0
        self.hyperparameters['weights'] = None
        self.hyperparameters['normailizer'] = lambda x: x

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            res = []
            for i in range(self.hyperparameters['#unit']):
                res.append(self.input['input'] @ self.hyperparameters['weights'][i])
            res = self.hyperparameters['normailizer'](res)
            self.outputBuffer['output'].set_val(res)
        except:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val("Error in OutputLayer")
            return