import math


class DiscontinuityInspector:
    def __init__(self, probe_count=4000):
        self._probe_count = probe_count

    def find_breakpoints(self, func, a, b):
        points = []
        step = (b - a) / self._probe_count

        for i in range(self._probe_count + 1):
            x = a + i * step
            try:
                y = func(x)
                if not math.isfinite(y):
                    points.append(x)
            except (ZeroDivisionError, ValueError, OverflowError):
                points.append(x)

        return self._compress(points)

    @staticmethod
    def is_divergent(func, breakpoints, probe=1e-5):
        for p in breakpoints:
            left = DiscontinuityInspector._safe_value(func, p - probe)
            right = DiscontinuityInspector._safe_value(func, p + probe)
            if left is None or right is None:
                continue
            if abs(left) > 1e8 or abs(right) > 1e8:
                return True
        return False

    @staticmethod
    def _safe_value(func, x):
        try:
            value = func(x)
            if not math.isfinite(value):
                return None
            return value
        except (ZeroDivisionError, ValueError, OverflowError):
            return None

    @staticmethod
    def _compress(points, merge_eps=1e-4):
        if not points:
            return []
        points.sort()
        compact = [points[0]]
        for p in points[1:]:
            if abs(p - compact[-1]) > merge_eps:
                compact.append(p)
        return compact
