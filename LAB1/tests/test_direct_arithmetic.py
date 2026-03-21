from decimal import Decimal

import pytest

from number_repr import DirectCodeArithmetic, IntegerCodes


def test_multiply_positive_and_negative():
    result = DirectCodeArithmetic.multiply(-7, 6)
    assert result['result_value'] == -42
    assert result['result_bits'][0] == 1
    assert result['a_bits'] == IntegerCodes.to_sign_magnitude(-7)


def test_multiply_zero():
    result = DirectCodeArithmetic.multiply(0, 99)
    assert result['result_value'] == 0


def test_multiply_overflow():
    with pytest.raises(OverflowError):
        DirectCodeArithmetic.multiply(1 << 20, 1 << 20)


def test_divide_positive():
    result = DirectCodeArithmetic.divide(22, 7)
    assert result['result_value'] == Decimal('3.14285')
    assert result['scaled_integer'] == 314285


def test_divide_negative():
    result = DirectCodeArithmetic.divide(-1, 8)
    assert result['result_value'] == Decimal('-0.12500')
    assert result['result_bits'][0] == 1


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        DirectCodeArithmetic.divide(1, 0)


def test_divide_scaled_overflow():
    with pytest.raises(OverflowError):
        DirectCodeArithmetic.divide((1 << 30) - 1, 1, precision=5)
