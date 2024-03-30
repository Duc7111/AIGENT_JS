
from Module import Module

class FileReader(Module):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.hyperparameters['file'] = file

    def run(self) -> None:
        try:
            file = open(self.hyperparameters['file'], 'r')
            self.outputBuffer['output'].set_val(id(self), file.read())
            self.status = True
        except:
            self.status = False
        finally:
            file.close()

class FileWriter(Module):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.hyperparameters['file'] = file

    def run(self) -> None:
        try:
            file = open(self.hyperparameters['file'], 'w')
            file.write(self.inputBuffer['input'].get_val(id(self)))
            self.status = True
        except:
            self.status = False
        finally:
            file.close()
