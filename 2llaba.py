from datetime import datetime
from typing import List


class PressureMeasurement:
    """Represents a single pressure measurement."""

    def __init__(self, date: str, height: float, value: int):
        self.date = date
        self.height = height
        self.value = value

    def date_as_datetime(self) -> datetime:
        """Converts date string to datetime object."""
        return datetime.strptime(self.date, "%Y.%m.%d")

    def display(self) -> None:
        """Prints the measurement in table format."""
        print(f"{self.date:12} | {self.height:8.1f} м | {self.value:6} Па")


class PressureParser:
    """Parses user input into PressureMeasurement objects."""

    @staticmethod
    def parse(input_str: str) -> PressureMeasurement:
        tokens = split_input(input_str)
        validate_token_count(tokens)

        date = parse_date(tokens[0])
        height = parse_height(tokens[1])
        value = parse_pressure(tokens[2])

        return PressureMeasurement(date, height, value)


def split_input(text: str) -> List[str]:
    """Splits user input into tokens."""
    return text.split()


def validate_token_count(tokens: List[str]) -> None:
    """Validates number of tokens."""
    if len(tokens) != 3:
        raise ValueError("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ")


def parse_date(date: str) -> str:
    """Validates and returns date."""
    try:
        datetime.strptime(date, "%Y.%m.%d")
        return date
    except ValueError:
        raise ValueError("Формат даты: ГГГГ.ММ.ДД")


def parse_height(value: str) -> float:
    """Parses and validates height."""
    height = float(value)
    if height < 0:
        raise ValueError("Высота не может быть отрицательной")
    return height


def parse_pressure(value: str) -> int:
    """Parses and validates pressure."""
    pressure = int(value)
    if pressure <= 0:
        raise ValueError("Давление должно быть положительным")
    return pressure


def show_header() -> None:
    """Prints application header."""
    print("\n=== БАЗА ИЗМЕРЕНИЙ ДАВЛЕНИЯ ===")


def show_menu() -> None:
    """Prints menu."""
    print("""
1 — Добавить измерение
2 — Показать все измерения
3 — Отсортировать по дате
4 — ТОП-5 максимальных давлений
0 — Выход
""")


def add_measurement(storage: List[PressureMeasurement]) -> None:
    """Adds a new measurement to storage."""
    try:
        user_input = input("Введите: ДАТА ВЫСОТА ЗНАЧЕНИЕ: ")
        storage.append(PressureParser.parse(user_input))
        print("Добавлено!\n")
    except ValueError as error:
        print("Ошибка:", error)


def print_table(data: List[PressureMeasurement]) -> None:
    """Prints measurements table."""
    if not data:
        print("Нет данных.")
        return

    print("\nДата         | Высота   | Давление")
    print("-" * 36)
    for item in data:
        item.display()
    print("-" * 36)


def sort_by_date(data: List[PressureMeasurement]) -> None:
    """Sorts measurements by date."""
    data.sort(key=lambda x: x.date_as_datetime())
    print("Отсортировано по дате.")


def show_top5(data: List[PressureMeasurement]) -> None:
    """Shows top 5 highest pressure values."""
    top = sorted(data, key=lambda x: x.value, reverse=True)[:5]
    print("\nТОП-5 максимальных давлений:")
    print_table(top)


def main() -> None:
    """Program entry point."""
    measurements: List[PressureMeasurement] = []

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
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
