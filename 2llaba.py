from datetime import datetime
from typing import List

DATA_FILE = "pressure_data.txt"


class PressureMeasurement:
    """Represents a single pressure measurement."""

    def __init__(self, date: str, height: float, value: int):
        self.date = date
        self.height = height
        self.value = value

    def date_as_datetime(self) -> datetime:
        return datetime.strptime(self.date, "%Y.%m.%d")

    def to_file_string(self) -> str:
        return f"{self.date} {self.height} {self.value}"

    @staticmethod
    def from_file_string(line: str):
        tokens = line.strip().split()
        return PressureMeasurement(tokens[0], float(tokens[1]), int(tokens[2]))

    def display(self) -> None:
        print(f"{self.date:12} | {self.height:8.1f} м | {self.value:6} Па")


class PressureParser:
    @staticmethod
    def parse(input_str: str) -> PressureMeasurement:
        tokens = split_input(input_str)
        validate_token_count(tokens)

        date = parse_date(tokens[0])
        height = parse_height(tokens[1])
        value = parse_pressure(tokens[2])

        return PressureMeasurement(date, height, value)


def split_input(text: str) -> List[str]:
    return text.split()


def validate_token_count(tokens: List[str]) -> None:
    if len(tokens) != 3:
        raise ValueError("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ")


def parse_date(date: str) -> str:
    try:
        datetime.strptime(date, "%Y.%m.%d")
        return date
    except ValueError:
        raise ValueError("Формат даты: ГГГГ.ММ.ДД")


def parse_height(value: str) -> float:
    height = float(value)
    if height < 0:
        raise ValueError("Высота не может быть отрицательной")
    return height


def parse_pressure(value: str) -> int:
    pressure = int(value)
    if pressure <= 0:
        raise ValueError("Давление должно быть положительным")
    return pressure


def show_header() -> None:
    print("\n=== БАЗА ИЗМЕРЕНИЙ ДАВЛЕНИЯ ===")


def show_menu() -> None:
    print("""
1 — Добавить измерение
2 — Показать все измерения
3 — Отсортировать по дате
4 — ТОП-5 максимальных давлений
0 — Выход
""")


def load_from_file() -> List[PressureMeasurement]:
    measurements = []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                measurements.append(PressureMeasurement.from_file_string(line))
    except FileNotFoundError:
        pass
    return measurements


def save_to_file(data: List[PressureMeasurement]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        for item in data:
            file.write(item.to_file_string() + "\n")


def add_measurement(storage: List[PressureMeasurement]) -> None:
    try:
        user_input = input("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ: ")
        storage.append(PressureParser.parse(user_input))
        save_to_file(storage)
        print("Добавлено!\n")
    except ValueError as error:
        print("Ошибка:", error)


def print_table(data: List[PressureMeasurement]) -> None:
    if not data:
        print("Нет данных.")
        return

    print("\nДата         | Высота   | Давление")
    print("-" * 36)
    for item in data:
        item.display()
    print("-" * 36)


def sort_by_date(data: List[PressureMeasurement]) -> None:
    data.sort(key=lambda x: x.date_as_datetime())
    save_to_file(data)
    print("Отсортировано по дате.")


def show_top5(data: List[PressureMeasurement]) -> None:
    top = sorted(data, key=lambda x: x.value, reverse=True)[:5]
    print("\nТОП-5 максимальных давлений:")
    print_table(top)


def main() -> None:
    measurements = load_from_file()
    show_header()

    while True:
        show_menu()
        choice = input("Выбор: ")

        if choice == "1":
            add_measurement(measurements)
        elif choice == "2":
            print_table(measurements)
        elif choice == "3":
            sort_by_date(measurements)
        elif choice == "4":
            show_top5(measurements)
        elif choice == "0":
            save_to_file(measurements)
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
