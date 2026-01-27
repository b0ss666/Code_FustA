import pytest
from main import PressureParser, InputError


def test_correct_input():
    m = PressureParser.parse("2025.01.10 150 760")
    assert m.height == 150
    assert m.value == 760


@pytest.mark.parametrize("text", [
    "",
    "2025.01.10 150",
    "hello world",
    "2025.01.10 -5 700",
    "2025.01.10 100 -10",
    "2025-01-10 100 700",
    "2025.01.32 100 700",
    "2025.01.10 ten 700"
])
def test_bad_inputs(text):
    with pytest.raises(InputError):
        PressureParser.parse(text)
