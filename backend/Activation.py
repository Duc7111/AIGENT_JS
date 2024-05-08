
from math import tanh, exp

def none(x: float) -> float:
    return x

def ReLU(x: float) -> float:
    return x if x > 0 else 0

def sigmoid(x: float) -> float:
    return 1 / (1 + exp(-x))

def tanh(x: float) -> float:
    return tanh(x)