import pytest

from number_repr import IntegerCodes


def test_sign_magnitude_roundtrip():
    value = -13
    bits = IntegerCodes.to_sign_magnitude(value)
    assert bits[0] == 1
    assert IntegerCodes.from_sign_magnitude(bits) == value


def test_ones_complement_roundtrip():
    value = -9
    bits = IntegerCodes.to_ones_complement(value)
    assert bits[0] == 1
    assert IntegerCodes.from_ones_complement(bits) == value


def test_twos_complement_roundtrip():
    value = -25
    bits = IntegerCodes.to_twos_complement(value)
    assert bits[0] == 1
    assert IntegerCodes.from_twos_complement(bits) == value


def test_positive_number_codes():
    value = 12
    assert IntegerCodes.to_sign_magnitude(value) == [0] * 28 + [1, 1, 0, 0]
    assert IntegerCodes.to_ones_complement(value) == [0] * 28 + [1, 1, 0, 0]
    assert IntegerCodes.to_twos_complement(value) == [0] * 28 + [1, 1, 0, 0]


def test_negative_number_codes():
    value = -5
    assert IntegerCodes.to_sign_magnitude(value) == [1] + [0] * 27 + [0, 1, 0, 1]
    assert IntegerCodes.to_ones_complement(value) == [1] * 29 + [0, 1, 0]
    assert IntegerCodes.to_twos_complement(value) == [1] * 29 + [0, 1, 1]


def test_add_without_overflow():
    result = IntegerCodes.add(17, -5)
    assert result['result_value'] == 12
    assert IntegerCodes.from_twos_complement(result['result_bits']) == 12


def test_add_with_overflow():
    with pytest.raises(OverflowError):
        IntegerCodes.add(2147483647, 1)


def test_subtract_without_overflow():
    result = IntegerCodes.subtract(17, 5)
    assert result['result_value'] == 12
    assert IntegerCodes.from_twos_complement(result['result_bits']) == 12


def test_subtract_with_overflow():
    with pytest.raises(OverflowError):
        IntegerCodes.subtract(-2147483648, 1)


def test_invalid_bit_length_for_decoding():
    with pytest.raises(ValueError):
        IntegerCodes.from_sign_magnitude([1, 0, 1])

    with pytest.raises(ValueError):
        IntegerCodes.from_ones_complement([1, 0, 1])

    with pytest.raises(ValueError):
        IntegerCodes.from_twos_complement([1, 0, 1])


def test_out_of_range_sign_magnitude():
    with pytest.raises(OverflowError):
        IntegerCodes.to_sign_magnitude(2147483648)

    with pytest.raises(OverflowError):
        IntegerCodes.to_ones_complement(-2147483648)


def test_out_of_range_twos_complement():
    with pytest.raises(OverflowError):
        IntegerCodes.to_twos_complement(2147483648)

    with pytest.raises(OverflowError):
        IntegerCodes.to_twos_complement(-2147483649)