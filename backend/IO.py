
from Module import Module
from Container import Buffer

class FileReader(Module):
    def __init__(self, file: str) -> None:
        super().__init__()
        self.hyperparameters['file'] = file
        self.outputBuffer['output'] = Buffer('')

    def run(self) -> None:
        super.run()
        if self.status == False:
            return
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
        super.run()
        if self.status == False:
            return
        try:
            file = open(self.hyperparameters['file'], 'w')
            file.write(self.inputBuffer['input'].get_val(id(self)))
            self.status = True
        except:
            self.status = False
        finally:
            file.close()

# take a string in hyperparameters and output it
class TextHolder(Module):
    def __init__(self, text: str) -> None:
        super().__init__()
        self.hyperparameters['text'] = text

    def run(self) -> None:
        super.run()
        if self.status == False:
            return
        self.outputBuffer['output'].set_val(id(self), self.hyperparameters['text'])
        self.status = True

# take a string in input and output it, kind of useless
class TextGetter(Module):
    def __init__(self) -> None:
        super().__init__()

    def run(self) -> None:
        super.run()
        if self.status == False:
            return
        self.outputBuffer['output'].set_val(id(self), self.inputBuffer['input'].get_val(id(self)))
        self.status = True

class VectorHolder(Module):
    def __init__(self, vector: list[int]) -> None:
        super().__init__()
        self.hyperparameters['vector'] = vector

    def run(self) -> None:
        super.run()
        if self.status == False:
            return
        self.outputBuffer['output'].set_val(id(self), self.hyperparameters['vector'])
        self.status = True

class MatrixHolder(Module):
    def __init__(self, matrix: list[list[int]]) -> None:
        super().__init__()
        self.hyperparameters['matrix'] = matrix

    def run(self) -> None:
        super.run()
        if self.status == False:
            return
        self.outputBuffer['output'].set_val(id(self), self.hyperparameters['matrix'])
        self.status = True