from decimal import Decimal

import pytest

from number_repr import BCD2421, Formatter


def test_encode_decode_digit():
    assert BCD2421.encode_digit(5) == [1, 0, 1, 1]
    assert BCD2421.decode_digit([1, 0, 1, 1]) == 5


def test_encode_decode_number():
    bits = BCD2421.encode_number(259)
    assert BCD2421.decode_number(bits) == 259


def test_bcd_addition():
    result = BCD2421.add(259, 481)
    assert result['result_value'] == 740
    assert BCD2421.decode_number(result['result_bits']) == 740


def test_bcd_addition_with_extra_carry_digit():
    result = BCD2421.add(999, 1)
    assert result['result_value'] == 1000
    assert BCD2421.decode_number(result['result_bits']) == 1000


def test_bcd_invalid_digit_and_length_and_negative():
    with pytest.raises(ValueError):
        BCD2421.encode_digit(10)
    with pytest.raises(ValueError):
        BCD2421.decode_digit([0, 1, 1, 1])
    with pytest.raises(ValueError):
        BCD2421.decode_number([0, 0, 0])
    with pytest.raises(ValueError):
        BCD2421.encode_number(-1)
    with pytest.raises(ValueError):
        BCD2421.add(-1, 2)


def test_internal_tetrad_addition():
    digit, carry = BCD2421._add_tetrads(BCD2421.encode_digit(8), BCD2421.encode_digit(7), 1)
    assert digit == 6
    assert carry == 1


def test_formatter_helpers():
    assert Formatter.bits([1, 0, 1]) == '101'
    assert Formatter.decimal(Decimal('3.14000')) == '3.14'
    assert Formatter.decimal(7) == '7'
    assert Formatter.report([1, 0], Decimal('2.500')) == {'binary': '10', 'decimal': '2.5'}