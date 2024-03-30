
from Module import Module

class FileReader(Module):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.hyperparameters['file'] = file

    def run(self) -> None:
        with open(self.hyperparameters['file'], 'r') as f:
            self.outputBuffer['output'] = f.read()

class FileWriter(Module):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.hyperparameters['file'] = file

    def run(self) -> None:
        with open(self.hyperparameters['file'], 'w') as f:
            f.write(self.inputBuffer['input'])