import math

from .models import Integrand


class FunctionRegistry:
    def __init__(self):
        self._functions = [
            Integrand("1", "x^3 - 2x + 1", lambda x: x**3 - 2 * x + 1),
            Integrand("2", "cos(x) + x", lambda x: math.cos(x) + x),
            Integrand("3", "exp(-x^2)", lambda x: math.exp(-(x**2))),
            Integrand("4", "ln(x + 2)", lambda x: math.log(x + 2)),
            Integrand("5", "3x^3 - 4x^2 + 7x - 17", lambda x: 3 * x**3 - 4 * x**2 + 7 * x - 17),
            Integrand("6", "1 / sqrt(x)    [0, 1], разрыв в точке a", lambda x: 1 / math.sqrt(x)),
            Integrand("7", "1 / sqrt(1 - x) [0, 1], разрыв в точке b", lambda x: 1 / math.sqrt(1 - x)),
            Integrand("8", "1 / (x - 0.5)^2 [0, 1], разрыв на отрезке", lambda x: 1 / ((x - 0.5) ** 2)),
        ]

    @property
    def items(self):
        return self._functions

    def show_menu(self):
        print("Список доступных функций:")
        for item in self._functions:
            print(f"  [{item.key}] {item.title}")

    def by_key(self, key):
        for item in self._functions:
            if item.key == key:
                return item
        raise ValueError("Неизвестный номер функции")
