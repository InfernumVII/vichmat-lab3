from .core.analysis import DiscontinuityInspector
from .core.calculators import ImproperIntegralCalculator, ProperIntegralCalculator
from .core.io import ConsoleIO, print_result
from .core.methods import QuadratureEngine
from .core.models import IntegrationError
from .core.registry import FunctionRegistry


class IntegrationApp:
    def __init__(self):
        self._registry = FunctionRegistry()
        self._engine = QuadratureEngine()
        self._proper_calculator = ProperIntegralCalculator(self._engine)
        self._improper_calculator = ImproperIntegralCalculator(self._engine)
        self._inspector = DiscontinuityInspector()

    def run(self):
        print("Численное интегрирование")
        print("Доступны схемы: прямоугольники, трапеции, Симпсон")
        print("Критерий остановки: оценка по правилу Рунге")

        integrand = self._choose_function()
        method = ConsoleIO.ask_method()
        a, b = ConsoleIO.ask_interval()
        eps = ConsoleIO.ask_positive_float("Задайте требуемую точность eps: ")

        try:
            self._process_integral(integrand, method, a, b, eps)
        except IntegrationError as exc:
            print(f"Сбой вычисления: {exc}")

        print("Расчет завершен.")

    def _choose_function(self):
        while True:
            self._registry.show_menu()
            selected = input("Номер функции: ").strip()
            try:
                return self._registry.by_key(selected)
            except ValueError:
                print("Нет такого пункта. Повторите выбор по меню.")

    def _process_integral(self, integrand, method, a, b, eps):
        breakpoints = self._inspector.find_breakpoints(integrand.value, a, b)

        if breakpoints:
            print("На интервале найдены точки разрыва.")
            if self._inspector.is_divergent(integrand.value, breakpoints):
                print("Интеграл не существует")
                return

            print("Интеграл сходится. Выполняю суммирование по частям интервала.")
            value, n = self._improper_calculator.calculate_method(method, integrand.value, a, b, eps, breakpoints)
        else:
            value, n = self._proper_calculator.calculate_method(method, integrand.value, a, b, eps)

        print_result(method, value, n)
