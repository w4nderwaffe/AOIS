from decimal import Decimal

import pytest

from number_repr import IEEE754Binary32


def assert_close_decimal(actual, expected, tolerance='0.000001'):
    assert abs(actual - Decimal(expected)) <= Decimal(tolerance)


def test_zero_roundtrip():
    bits = IEEE754Binary32.from_decimal('0')
    assert bits == [0] * 32
    assert IEEE754Binary32.to_decimal(bits) == 0


def test_positive_roundtrip():
    bits = IEEE754Binary32.from_decimal('5.75')
    assert bits[0] == 0
    assert_close_decimal(IEEE754Binary32.to_decimal(bits), '5.75')


def test_negative_roundtrip():
    bits = IEEE754Binary32.from_decimal('-0.15625')
    assert bits[0] == 1
    assert_close_decimal(IEEE754Binary32.to_decimal(bits), '-0.15625')


def test_subnormal_roundtrip():
    bits = IEEE754Binary32.from_decimal('1e-40')
    assert bits[1:9] == [0] * 8
    assert_close_decimal(IEEE754Binary32.to_decimal(bits), '1e-40', '1e-42')


def test_underflow_to_zero():
    bits = IEEE754Binary32.from_decimal('1e-50')
    assert bits == [0] * 32


def test_overflow_error():
    with pytest.raises(OverflowError):
        IEEE754Binary32.from_decimal('1e50')


def test_addition_operation():
    result = IEEE754Binary32.add('1.5', '2.25')
    assert_close_decimal(result['result_value'], '3.75')


def test_subtraction_operation():
    result = IEEE754Binary32.subtract('5.5', '2.25')
    assert_close_decimal(result['result_value'], '3.25')


def test_subtraction_to_zero():
    result = IEEE754Binary32.subtract('2.5', '2.5')
    assert result['result_bits'] == [0] * 32
    assert result['result_value'] == 0


def test_multiplication_operation():
    result = IEEE754Binary32.multiply('1.5', '-2')
    assert_close_decimal(result['result_value'], '-3')


def test_division_operation():
    result = IEEE754Binary32.divide('7', '2')
    assert_close_decimal(result['result_value'], '3.5')


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        IEEE754Binary32.divide('1', '0')


def test_nan_or_infinity_conversion_error():
    with pytest.raises(ValueError):
        IEEE754Binary32.to_decimal([0] + [1] * 8 + [0] * 23)


def test_add_bits_with_zero_shortcut():
    zero = [0] * 32
    value = IEEE754Binary32.from_decimal('4.5')
    assert IEEE754Binary32.add_bits(zero, value) == value
    assert IEEE754Binary32.add_bits(value, zero) == value


def test_manual_bit_operations_match_public_operations():
    a_bits = IEEE754Binary32.from_decimal('6.25')
    b_bits = IEEE754Binary32.from_decimal('-1.5')
    assert_close_decimal(IEEE754Binary32.to_decimal(IEEE754Binary32.add_bits(a_bits, b_bits)), '4.75')
    assert_close_decimal(IEEE754Binary32.to_decimal(IEEE754Binary32.subtract_bits(a_bits, b_bits)), '7.75')
    assert_close_decimal(IEEE754Binary32.to_decimal(IEEE754Binary32.multiply_bits(a_bits, b_bits)), '-9.375')
    assert_close_decimal(IEEE754Binary32.to_decimal(IEEE754Binary32.divide_bits(a_bits, IEEE754Binary32.from_decimal('2'))), '3.125')


def test_negate_preserves_zero():
    assert IEEE754Binary32._negate([0] * 32) == [0] * 32


def test_unpack_rejects_special_value():
    with pytest.raises(ValueError):
        IEEE754Binary32._unpack([0] + [1] * 8 + [0] * 23)