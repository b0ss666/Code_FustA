from datetime import datetime
from typing import List, Iterable

DATA_FILE = "pressure_data.txt"


class InputError(Exception):
    """User input validation error."""


class PressureMeasurement:
    """Represents a single pressure measurement."""

    __slots__ = ("date", "height", "value")

    def __init__(self, date: str, height: float, value: int):
        self.date = date
        self.height = height
        self.value = value

    def date_as_datetime(self) -> datetime:
        return datetime.strptime(self.date, "%Y.%m.%d")

    def to_file_string(self) -> str:
        return f"{self.date} {self.height} {self.value}"

    @staticmethod
    def from_file_string(line: str) -> "PressureMeasurement":
        parts = line.strip().split()
        if len(parts) != 3:
            raise InputError("Повреждённая строка в файле")
        return PressureMeasurement(parts[0], float(parts[1]), int(parts[2]))

    def display(self) -> None:
        print(f"{self.date:12} | {self.height:8.1f} м | {self.value:6} Па")


class MeasurementRepository:
    """Stores and persists measurements."""

    def __init__(self, filename: str):
        self.filename = filename
        self._data = self._load()

    def _load(self) -> List[PressureMeasurement]:
        result = []
        try:
            with open(self.filename, encoding="utf-8") as file:
                for line in file:
                    try:
                        result.append(PressureMeasurement.from_file_string(line))
                    except InputError:
                        continue
        except FileNotFoundError:
            pass
        return result

    def save(self) -> None:
        with open(self.filename, "w", encoding="utf-8") as file:
            for item in self._data:
                file.write(item.to_file_string() + "\n")

    def add(self, measurement: PressureMeasurement) -> None:
        self._data.append(measurement)
        self.save()

    def all(self) -> Iterable[PressureMeasurement]:
        return self._data


class PressureParser:
    """Parses and validates user input."""

    @staticmethod
    def parse(text: str) -> PressureMeasurement:
        parts = text.split()
        if len(parts) != 3:
            raise InputError("Введите: ДАТА ВЫСОТА ДАВЛЕНИЕ")

        date = parse_date(parts[0])
        height = parse_height(parts[1])
        value = parse_pressure(parts[2])
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


def print_table(data: Iterable[PressureMeasurement]) -> None:
    print("\nДата         | Высота   | Давление")
    print("-" * 36)
    empty = True
    for m in data:
        m.display()
        empty = False
    if empty:
        print("Нет данных.")
    print("-" * 36)


def show_top5(repo: MeasurementRepository) -> None:
    top = sorted(repo.all(), key=lambda x: x.value, reverse=True)[:5]
    print("\nТОП-5 максимальных давлений:")
    print_table(top)


def main() -> None:
    repo = MeasurementRepository(DATA_FILE)
    print("\n=== БАЗА ИЗМЕРЕНИЙ ДАВЛЕНИЯ ===")

    while True:
        print("""
1 — Добавить измерение
2 — Показать все измерения
3 — ТОП-5 максимальных давлений
0 — Выход
""")
        choice = input("Выбор: ")

        if choice == "1":
            try:
                text = input("Введите: ДАТА ВЫСОТА ДАВЛЕНИЕ: ")
                repo.add(PressureParser.parse(text))
                print("Добавлено.")
            except InputError as e:
                print("Ошибка:", e)
        elif choice == "2":
            print_table(repo.all())
        elif choice == "3":
            show_top5(repo)
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню.")


if __name__ == "__main__":
    main()
