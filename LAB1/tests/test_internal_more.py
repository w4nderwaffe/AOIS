from decimal import Decimal

import main
import pytest

from number_repr import BitArray32, DirectCodeArithmetic, IEEE754Binary32


def test_bit_array_zero_and_negative_compare_branch():
    assert BitArray32.zero() == [0] * 32
    with pytest.raises(ValueError):
        BitArray32.compare_unsigned([1], [1, 0])


def test_direct_unsigned_subtract_and_error():
    assert DirectCodeArithmetic._unsigned_subtract([1, 0, 1, 0], [0, 0, 1, 1]) == [0, 1, 1, 1]
    with pytest.raises(ValueError):
        DirectCodeArithmetic._unsigned_subtract([0, 0, 1], [0, 1, 0])


def test_direct_unsigned_add():
    result, carry = DirectCodeArithmetic._unsigned_add([0, 1, 0, 1], [0, 0, 1, 1])
    assert result == [1, 0, 0, 0]
    assert carry == 0


def test_ieee_helper_primitives():
    exp, normalized = IEEE754Binary32._normalize_decimal(Decimal('10'))
    assert exp == 3
    assert normalized == Decimal('1.25')
    assert IEEE754Binary32._normalize_decimal(Decimal('0')) == (0, Decimal('0'))

    bits, rest = IEEE754Binary32._fraction_to_bits(Decimal('0.625'), 4)
    assert bits == [1, 0, 1, 0]
    assert rest == 0

    rounded, carry = IEEE754Binary32._round_fraction_with_guard([1, 1, 1], 1, 0)
    assert rounded == [0, 0, 0]
    assert carry == 1

    rounded, carry = IEEE754Binary32._round_fraction_with_guard([1, 0, 0], 0, 1)
    assert rounded == [1, 0, 0]
    assert carry == 0


def test_ieee_shift_helpers_and_pack_edges():
    assert IEEE754Binary32._shift_right_round_even(9, 1) == 4
    assert IEEE754Binary32._shift_right_round_even(11, 1) == 6
    assert IEEE754Binary32._shift_right_round_even(3, -1) == 6
    assert IEEE754Binary32._shift_right_with_sticky(0, 5) == 0
    assert IEEE754Binary32._shift_right_with_sticky(8, 10) == 1

    normal = IEEE754Binary32._pack(0, 1 << 23, 0, 23)
    assert IEEE754Binary32.to_decimal(normal) == 1

    subnormal = IEEE754Binary32._pack(0, 1, -149, 0)
    assert subnormal[1:9] == [0] * 8
    assert IEEE754Binary32.to_decimal(subnormal) == Decimal(2) ** Decimal(-149)

    with pytest.raises(OverflowError):
        IEEE754Binary32._pack(0, 1 << 23, 200, 23)


def test_main_runs_and_prints(monkeypatch, capsys):
    inputs = iter(['12', '-5', '3.5', '1.25', '259', '481'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main.main()
    captured = capsys.readouterr().out
    assert 'Коды числа' in captured
    assert 'IEEE-754 сложение' in captured
    assert 'BCD 2421 сложение' in captured