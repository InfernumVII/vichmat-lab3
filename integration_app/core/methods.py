from .models import IntegrationError


class QuadratureEngine:
    RUNGE_DENOMINATOR = {
        "left_rectangle": 1,
        "right_rectangle": 1,
        "midpoint_rectangle": 3,
        "trapezoid": 3,
        "simpson": 15,
    }

    def left_rectangle(self, func, a, b, n):
        h = (b - a) / n
        total = 0.0
        for i in range(n):
            total += func(a + i * h)
        return total * h

    def right_rectangle(self, func, a, b, n):
        h = (b - a) / n
        total = 0.0
        for i in range(1, n + 1):
            total += func(a + i * h)
        return total * h

    def midpoint_rectangle(self, func, a, b, n):
        h = (b - a) / n
        total = 0.0
        for i in range(n):
            total += func(a + (i + 0.5) * h)
        return total * h

    def trapezoid(self, func, a, b, n):
        h = (b - a) / n
        total = (func(a) + func(b)) / 2
        for i in range(1, n):
            total += func(a + i * h)
        return total * h

    def simpson(self, func, a, b, n):
        if n % 2 != 0:
            n += 1
        h = (b - a) / n
        total = func(a) + func(b)
        for i in range(1, n):
            total += (4 if i % 2 else 2) * func(a + i * h)
        return total * h / 3

    def compute(self, method, func, a, b, n):
        methods = {
            "left_rectangle": self.left_rectangle,
            "right_rectangle": self.right_rectangle,
            "midpoint_rectangle": self.midpoint_rectangle,
            "trapezoid": self.trapezoid,
            "simpson": self.simpson,
        }
        if method not in methods:
            raise ValueError("Неизвестный метод")
        return methods[method](func, a, b, n)

    def adaptive_with_runge(
        self,
        method,
        func,
        a,
        b,
        eps,
        n0=4,
        max_iterations=30,
    ):
        n = n0
        previous = self.compute(method, func, a, b, n)

        for _ in range(max_iterations):
            n *= 2
            current = self.compute(method, func, a, b, n)
            error = abs(current - previous) / self.RUNGE_DENOMINATOR[method]
            if error <= eps:
                return current, n
            previous = current

        raise IntegrationError("Не удалось достичь требуемой точности за допустимое число итераций")
