import math


class IntegrationError(Exception):
    """Raised when numerical integration cannot be completed."""


class Integrand:
    def __init__(self, key, title, evaluator):
        self.key = key
        self.title = title
        self.evaluator = evaluator

    def value(self, x):
        y = self.evaluator(x)
        if not math.isfinite(y):
            raise ValueError("Function value is not finite")
        return y
