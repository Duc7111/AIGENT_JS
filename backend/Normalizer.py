
from math import tanh, exp

def none(x: float) -> float:
    return x

def softmax(x: list[float]) -> list[float]:
    res = []
    sum = 0
    for i in x:
        sum += exp(i)
    for i in x:
        res.append(exp(i) / sum)
    return res

