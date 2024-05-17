
from Module import Module
from Container import Buffer

class FileReader(Module):
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('file')
        self.hyperparameters['file'] = ""
        self.outputBuffer['output'] = Buffer('')

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            with open(self.hyperparameters['file'], 'r') as file:
                self.outputBuffer['output'].set_val(file.read())
                self.status = True
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))

class FileWriter(Module):
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('file')
        self.hyperparameters['file'] = ""
        self.inputBuffer['input'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            with open(self.hyperparameters['file'], 'w') as file:
                file.write(self.inputBuffer['input'].get_val(1))
                self.status = True
        except Exception as e:
            self.status = False
            self.outputBuffer['msg'].set_val(str(e))

# take a string in hyperparameters and output it
class TextHolder(Module):
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('text')
        self.hyperparameters['text'] = ""
        self.outputBuffer['output'] = Buffer('')

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            self.outputBuffer['output'].set_val(self.hyperparameters['text'])
            self.status = True
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))

# take a string in input and output it, kind of useless
class TextGetter(Module):
    def __init__(self) -> None:
        super().__init__()
        self.outputBuffer['output'] = Buffer('')
        self.inputBuffer['input'] = None

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            self.outputBuffer['output'].set_val(self.inputBuffer['input'].get_val(1))
            self.status = True
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))

class VectorHolder(Module):
    def __init__(self) -> None:
        super().__init__()
        self.hyperparameters_list = ('vector')
        self.hyperparameters['vector'] = []
        self.outputBuffer['output'] = Buffer([])

    def run(self) -> None:
        super().run()
        if self.status == False:
            return
        try:
            self.outputBuffer['output'].set_val(self.hyperparameters['vector'])
            self.status = True
        except Exception as e:
            self.status = False
            self.outputBuffer['output'].set_val(None)
            self.outputBuffer['msg'].set_val(str(e))

    def set_hyperparameters(self, hyperparameters: dict[str, any]) -> bool:
        if not super().set_hyperparameters(hyperparameters):
            return False
        if not isinstance(self.hyperparameters['vector'], list):
            return False
        return True
