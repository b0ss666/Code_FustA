from datetime import datetime


class PressureMeasurement:
    def __init__(self, date: str, height: float, value: int):
        self.date = date
        self.height = height
        self.value = value

    def date_as_datetime(self):
        return datetime.strptime(self.date, "%Y.%m.%d")

    def display(self) -> None:
        print(f"{self.date:12} | {self.height:8} м | {self.value:6} Па")


class PressureParser:
    @staticmethod
    def parse(input_str: str) -> PressureMeasurement:
        tokens = input_str.split()

        if len(tokens) != 3:
            raise ValueError("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ")

        date = tokens[0]
        if len(date) != 10 or date[4] != '.' or date[7] != '.':
            raise ValueError("Формат даты: ГГГГ.ММ.ДД")

        height = float(tokens[1])
        value = int(tokens[2])

        if height < 0:
            raise ValueError("Высота не может быть отрицательной")
        if value <= 0:
            raise ValueError("Давление должно быть положительным")

        return PressureMeasurement(date, height, value)


def show_header():
    print("\n=== БАЗА ИЗМЕРЕНИЙ ДАВЛЕНИЯ ===")


def show_menu():
    print("""
1 — Добавить измерение
2 — Показать все измерения
3 — Отсортировать по дате
4 — ТОП-5 максимальных давлений
0 — Выход
""")


def print_table(data):
    if not data:
        print("Нет данных.")
        return
    print("\nДата         | Высота   | Давление")
    print("-" * 36)
    for m in data:
        m.display()
    print("-" * 36)


def main():
    measurements = []

    show_header()

    while True:
        show_menu()
        choice = input("Выбор: ")

        if choice == "1":
            try:
                inp = input("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ: ")
                m = PressureParser.parse(inp)
                measurements.append(m)
                print("Добавлено!\n")
            except ValueError as e:
                print("Ошибка:", e)

        elif choice == "2":
            print_table(measurements)

        elif choice == "3":
            measurements.sort(key=lambda x: x.date_as_datetime())
            print("Отсортировано по дате.")

        elif choice == "4":
            top5 = sorted(measurements, key=lambda x: x.value, reverse=True)[:5]
            print("\nТОП-5 максимальных давлений:")
            print_table(top5)

        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
