class ConsoleIO:
    @staticmethod
    def ask_float(prompt):
        while True:
            raw = input(prompt).strip().replace(",", ".")
            try:
                return float(raw)
            except ValueError:
                print("Ожидалось число. Введите значение еще раз.")

    @staticmethod
    def ask_positive_float(prompt):
        while True:
            value = ConsoleIO.ask_float(prompt)
            if value > 0:
                return value
            print("eps должно быть строго больше нуля.")

    @staticmethod
    def ask_interval():
        while True:
            a = ConsoleIO.ask_float("Левая граница a: ")
            b = ConsoleIO.ask_float("Правая граница b: ")
            if a < b:
                return a, b
            print("Неверный интервал: требуется a < b.")

    @staticmethod
    def ask_method():
        methods = {
            "1": "left_rectangle",
            "2": "right_rectangle",
            "3": "midpoint_rectangle",
            "4": "trapezoid",
            "5": "simpson",
        }

        print("Выберите метод интегрирования:")
        print("  [1] Левые прямоугольники")
        print("  [2] Правые прямоугольники")
        print("  [3] Средние прямоугольники")
        print("  [4] Трапеции")
        print("  [5] Симпсон")

        while True:
            choice = input("Номер метода: ").strip()
            if choice in methods:
                return methods[choice]
            print("Нет такого метода. Повторите выбор.")


def print_results(results):
    readable_names = {
        "left_rectangle": "Левые прямоугольники",
        "right_rectangle": "Правые прямоугольники",
        "midpoint_rectangle": "Средние прямоугольники",
        "trapezoid": "Трапеции",
        "simpson": "Симпсон",
    }

    print("\nИтог по методам:")
    for method, (value, n) in results.items():
        print(f"{readable_names[method]} -> I ~= {value:.10f}; разбиений: {n}")


def print_result(method, value, n):
    readable_names = {
        "left_rectangle": "Левые прямоугольники",
        "right_rectangle": "Правые прямоугольники",
        "midpoint_rectangle": "Средние прямоугольники",
        "trapezoid": "Трапеции",
        "simpson": "Симпсон",
    }

    print("\nИтог расчета:")
    print(f"Метод: {readable_names[method]}")
    print(f"I ~= {value:.10f}")
    print(f"Разбиений: {n}")
