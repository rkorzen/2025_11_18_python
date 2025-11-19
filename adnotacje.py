class Data:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b

    def info(self) -> str:
        return f"a={self.a}, b={self.b}"



d = Data(1, 2)



def func(x: int, y: int) -> Data:
    d = (1, 2)
    return d



result = func("A", 'B')

from typing import Optional

def op(a: int, b: int, type: str) -> int | float | None:
    if type == "+":
        return a + b
    elif type == "/":
        return a / b
    return None

numeric = int | float | complex

def op(a: numeric, b: numeric, type: str) -> Optional[numeric]:
    if type == "+":
        return a + b
    elif type == "/":
        return a / b
    return None

from typing import Union
numeric = Union[int, float, complex]