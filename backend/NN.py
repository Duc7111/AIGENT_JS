
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
            return
        
