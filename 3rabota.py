from datetime import datetime
from typing import List

DATA_FILE = "pressure_data.txt"


class InputError(Exception):
    """User input error."""
    pass


class PressureMeasurement:
    """Single pressure measurement."""

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


class MeasurementRepository:
    """Handles data persistence."""

    def __init__(self, filename: str):
        self.filename = filename
        self.data = self._load()

    def _load(self) -> List[PressureMeasurement]:
        result = []
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        result.append(
                            PressureMeasurement.from_file_string(line)
                        )
                    except Exception:
                        pass
        except FileNotFoundError:
            pass
        return result

    def save(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            for item in self.data:
                file.write(item.to_file_string() + "\n")

    def add(self, measurement: PressureMeasurement) -> None:
        self.data.append(measurement)
        self.save()


class PressureParser:
    """Parses and validates user input."""

    @staticmethod
    def parse(text: str) -> PressureMeasurement:
        tokens = text.split()
        if len(tokens) != 3:
            raise InputError("Введите: ДАТА ВЫСОТА ДАВЛЕНИЕ")

        date = parse_date(tokens[0])
        height = parse_height(tokens[1])
        value = parse_pressure(tokens[2])

        return PressureMeasurement(date, height, value)


def parse_date(text: str) -> str:
    try:
        datetime.strptime(text, "%Y.%m.%d")
        return text
    except ValueError:
        raise InputError("Формат даты: ГГГГ.ММ.ДД")


def parse_height(text: str) -> float:
    try:
        value = float(text)
    except ValueError:
        raise InputError("Высота должна быть числом")

    if value < 0:
        raise InputError("Высота не может быть отрицательной")
    return value


def parse_pressure(text: str) -> int:
    try:
        value = int(text)
    except ValueError:
        raise InputError("Давление должно быть целым числом")

    if value <= 0:
        raise InputError("Давление должно быть положительным")
    return value


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


def print_table(data: List[PressureMeasurement]):
    if not data:
        print("Нет данных.")
        return

    print("\nДата         | Высота   | Давление")
    print("-" * 36)
    for m in data:
        m.display()
    print("-" * 36)


def add_measurement_ui(repo: MeasurementRepository):
    try:
        text = input("Введите: ДАТА ВЫСОТА ДАВЛЕНИЕ: ")
        m = PressureParser.parse(text)
        repo.add(m)
        print("Добавлено.")
    except InputError as e:
        print("Ошибка:", e)


def sort_by_date(repo: MeasurementRepository):
    repo.data.sort(key=lambda x: x.date_as_datetime())
    repo.save()
    print("Отсортировано по дате.")


def show_top5(repo: MeasurementRepository):
    top = sorted(repo.data, key=lambda x: x.value, reverse=True)[:5]
    print("\nТОП-5 максимальных давлений:")
    print_table(top)


def main():
    repo = MeasurementRepository(DATA_FILE)
    show_header()

    while True:
        show_menu()
        choice = input("Выбор: ")

        if choice == "1":
            add_measurement_ui(repo)
        elif choice == "2":
            print_table(repo.data)
        elif choice == "3":
            sort_by_date(repo)
        elif choice == "4":
            show_top5(repo)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
