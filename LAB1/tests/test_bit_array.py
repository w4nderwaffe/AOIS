import pytest

from number_repr import BitArray32


def test_unsigned_roundtrip():
    bits = BitArray32.from_unsigned_int(13, 8)
    assert bits == [0, 0, 0, 0, 1, 1, 0, 1]
    assert BitArray32.to_unsigned_int(bits) == 13


def test_from_unsigned_int_negative_error():
    with pytest.raises(ValueError):
        BitArray32.from_unsigned_int(-1)


def test_from_unsigned_int_overflow_error():
    with pytest.raises(OverflowError):
        BitArray32.from_unsigned_int(8, 3)


def test_add_bits_and_add_one_and_compare():
    a = [0, 1, 1, 1]
    b = [0, 0, 0, 1]
    result, carry = BitArray32.add_bits(a, b)
    assert result == [1, 0, 0, 0]
    assert carry == 0
    assert BitArray32.add_one([1, 1, 1, 1]) == [0, 0, 0, 0]
    assert BitArray32.compare_unsigned([0, 1], [1, 0]) == -1
    assert BitArray32.compare_unsigned([1, 0], [0, 1]) == 1
    assert BitArray32.compare_unsigned([1, 0], [1, 0]) == 0


def test_add_bits_length_error():
    with pytest.raises(ValueError):
        BitArray32.add_bits([0], [0, 1])


def test_shift_and_zero_checks():
    bits = [1, 0, 1, 1]
    assert BitArray32.shift_left(bits, 2) == [1, 1, 0, 0]
    assert BitArray32.shift_right_logical(bits, 2) == [0, 0, 1, 0]
    assert BitArray32.shift_left(bits, 10) == [0, 0, 0, 0]
    assert BitArray32.shift_right_logical(bits, 10) == [0, 0, 0, 0]
    assert BitArray32.is_zero([0, 0, 0]) is True
    assert BitArray32.is_zero([0, 1, 0]) is False


def test_negative_shift_error():
    with pytest.raises(ValueError):
        BitArray32.shift_left([1, 0], -1)
    with pytest.raises(ValueError):
        BitArray32.shift_right_logical([1, 0], -1)


def test_to_string_and_invert():
    bits = [1, 0, 1, 0]
    assert BitArray32.to_string(bits) == '1010'
    assert BitArray32.invert(bits) == [0, 1, 0, 1]
