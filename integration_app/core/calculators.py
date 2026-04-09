from .methods import QuadratureEngine
from .models import IntegrationError


METHODS = [
    "left_rectangle",
    "right_rectangle",
    "midpoint_rectangle",
    "trapezoid",
    "simpson",
]


class ProperIntegralCalculator:
    def __init__(self, engine):
        self._engine = engine

    def calculate_all_methods(
        self,
        func,
        a,
        b,
        eps,
    ):
        results = {}
        for method in METHODS:
            results[method] = self._engine.adaptive_with_runge(method, func, a, b, eps)
        return results

    def calculate_method(self, method, func, a, b, eps):
        return self._engine.adaptive_with_runge(method, func, a, b, eps)


class ImproperIntegralCalculator:
    def __init__(self, engine):
        self._engine = engine

    def calculate_all_methods(
        self,
        func,
        a,
        b,
        eps,
        breakpoints,
        delta=1e-6,
    ):
        segments = self._build_segments(a, b, breakpoints, delta)
        if not segments:
            raise IntegrationError("Интервал выродился после исключения разрывов")

        results = {}
        for method in METHODS:
            total_value = 0.0
            total_n = 0
            for left, right in segments:
                value, n = self._engine.adaptive_with_runge(method, func, left, right, eps)
                total_value += value
                total_n += n
            results[method] = (total_value, total_n)

        return results

    def calculate_method(
        self,
        method,
        func,
        a,
        b,
        eps,
        breakpoints,
        delta=1e-6,
    ):
        segments = self._build_segments(a, b, breakpoints, delta)
        if not segments:
            raise IntegrationError("Интервал выродился после исключения разрывов")

        total_value = 0.0
        total_n = 0
        for left, right in segments:
            value, n = self._engine.adaptive_with_runge(method, func, left, right, eps)
            total_value += value
            total_n += n

        return total_value, total_n

    @staticmethod
    def _build_segments(a, b, breakpoints, delta):
        if not breakpoints:
            return [(a, b)]

        left_edge = a
        right_edge = b

        for point in breakpoints:
            if abs(point - a) <= delta * 10:
                left_edge = a + delta
            if abs(point - b) <= delta * 10:
                right_edge = b - delta

        if left_edge >= right_edge:
            return []

        safe_points = [p for p in breakpoints if left_edge < p < right_edge]
        if not safe_points:
            return [(left_edge, right_edge)]

        segments = []
        current = left_edge

        for p in safe_points:
            left = current
            right = p - delta
            if right > left:
                segments.append((left, right))
            current = p + delta

        if current < right_edge:
            segments.append((current, right_edge))

        return segments
