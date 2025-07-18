import pytest

from tools.math_calculator import calculator
from utils.errors import ToolError


def test_calculator_success() -> None:
    result = calculator("3 * (4 + 2)")
    assert result == "18"


def test_calculator_failure() -> None:
    with pytest.raises(ToolError):
        calculator("X + Y")
