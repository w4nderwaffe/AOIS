from decimal import Decimal, getcontext

from .bit_array import BitArray32

getcontext().prec = 200

BIAS = 127
FRACTION_BITS = 23
EXP_BITS = 8
MIN_NORMAL_EXP = -126
MAX_NORMAL_EXP = 127
MIN_SUBNORMAL = Decimal(2) ** Decimal(-149)


class IEEE754Binary32:
    @staticmethod
    def _normalize_decimal(value: Decimal):
        if value == 0:
            return 0, Decimal(0)
        exp = 0
        magnitude = abs(value)
        while magnitude >= 2:
            magnitude /= 2
            exp += 1
        while magnitude < 1:
            magnitude *= 2
            exp -= 1
        return exp, magnitude

    @staticmethod
    def _fraction_to_bits(frac: Decimal, count: int):
        bits = []
        value = frac
        for _ in range(count):
            value *= 2
            if value >= 1:
                bits.append(1)
                value -= 1
            else:
                bits.append(0)
        return bits, value

    @staticmethod
    def _round_fraction_with_guard(main_bits, guard_bit, sticky_bit):
        rounded = main_bits[:]
        lsb = rounded[-1] if rounded else 0
        if guard_bit == 1 and (sticky_bit == 1 or lsb == 1):
            carry = 1
            for i in range(len(rounded) - 1, -1, -1):
                total = rounded[i] + carry
                rounded[i] = total % 2
                carry = total // 2
            return rounded, carry
        return rounded, 0

    @staticmethod
    def _unpack(bits):
        exponent_raw = BitArray32.to_unsigned_int(bits[1:9])
        fraction = BitArray32.to_unsigned_int(bits[9:])
        if exponent_raw == 0:
            if fraction == 0:
                return bits[0], MIN_NORMAL_EXP, 0
            return bits[0], MIN_NORMAL_EXP, fraction
        if exponent_raw == 255:
            raise ValueError('Infinity and NaN are not supported')
        return bits[0], exponent_raw - BIAS, (1 << FRACTION_BITS) + fraction

    @staticmethod
    def _pack(sign: int, mantissa: int, exponent: int, scale_bits: int):
        if mantissa == 0:
            return [0] * 32

        leading = mantissa.bit_length() - 1
        unbiased_exp = exponent - scale_bits + leading

        if leading > FRACTION_BITS:
            mantissa = IEEE754Binary32._shift_right_round_even(mantissa, leading - FRACTION_BITS)
        elif leading < FRACTION_BITS:
            mantissa <<= FRACTION_BITS - leading

        if mantissa >= (1 << (FRACTION_BITS + 1)):
            mantissa >>= 1
            unbiased_exp += 1

        if unbiased_exp > MAX_NORMAL_EXP:
            raise OverflowError('Value is too large for binary32')

        if unbiased_exp >= MIN_NORMAL_EXP:
            exponent_bits = BitArray32.from_unsigned_int(unbiased_exp + BIAS, EXP_BITS)
            fraction_bits = BitArray32.from_unsigned_int(mantissa - (1 << FRACTION_BITS), FRACTION_BITS)
            return [sign] + exponent_bits + fraction_bits

        shift = MIN_NORMAL_EXP - unbiased_exp
        if shift >= FRACTION_BITS + 2:
            rounded = IEEE754Binary32._shift_right_round_even(mantissa, shift)
        else:
            rounded = IEEE754Binary32._shift_right_round_even(mantissa, shift)
        if rounded == 0:
            return [0] * 32
        if rounded >= (1 << FRACTION_BITS):
            exponent_bits = BitArray32.from_unsigned_int(1, EXP_BITS)
            return [sign] + exponent_bits + [0] * FRACTION_BITS
        return [sign] + [0] * EXP_BITS + BitArray32.from_unsigned_int(rounded, FRACTION_BITS)

    @staticmethod
    def _shift_right_round_even(value: int, shift: int):
        if shift <= 0:
            return value << (-shift)
        if value == 0:
            return 0
        truncated = value >> shift
        remainder = value & ((1 << shift) - 1)
        half = 1 << (shift - 1)
        if remainder > half or (remainder == half and (truncated & 1) == 1):
            truncated += 1
        return truncated

    @staticmethod
    def _shift_right_with_sticky(value: int, shift: int):
        if shift <= 0:
            return value << (-shift)
        if value == 0:
            return 0
        if shift >= value.bit_length() + 1:
            return 1
        shifted = value >> shift
        if value & ((1 << shift) - 1):
            shifted |= 1
        return shifted

    @staticmethod
    def from_decimal(value):
        dec_value = Decimal(str(value))
        if dec_value == 0:
            return [0] * 32
        sign = 1 if dec_value < 0 else 0
        magnitude = abs(dec_value)
        if magnitude > Decimal(0) and magnitude < MIN_SUBNORMAL:
            return [sign] + [0] * 31
        exp, normalized = IEEE754Binary32._normalize_decimal(magnitude)
        if exp > MAX_NORMAL_EXP:
            raise OverflowError('Value is too large for binary32')
        if exp < MIN_NORMAL_EXP:
            scaled = magnitude / MIN_SUBNORMAL
            integer = int(scaled)
            rest = scaled - Decimal(integer)
            bits = BitArray32.from_unsigned_int(integer, FRACTION_BITS)
            if rest > Decimal('0.5') or (rest == Decimal('0.5') and bits[-1] == 1):
                bits = BitArray32.add_one(bits)
                if BitArray32.to_unsigned_int(bits) == (1 << FRACTION_BITS):
                    exponent_bits = BitArray32.from_unsigned_int(1, EXP_BITS)
                    return [sign] + exponent_bits + [0] * FRACTION_BITS
            return [sign] + [0] * EXP_BITS + bits
        fraction = normalized - 1
        raw_bits, remainder = IEEE754Binary32._fraction_to_bits(fraction, FRACTION_BITS + 2)
        main_bits = raw_bits[:FRACTION_BITS]
        guard_bit = raw_bits[FRACTION_BITS]
        sticky_bit = raw_bits[FRACTION_BITS + 1] or (1 if remainder != 0 else 0)
        rounded_bits, carry = IEEE754Binary32._round_fraction_with_guard(main_bits, guard_bit, sticky_bit)
        exponent = exp + BIAS + carry
        if exponent >= 255:
            raise OverflowError('Value is too large for binary32')
        exponent_bits = BitArray32.from_unsigned_int(exponent, EXP_BITS)
        if carry:
            rounded_bits = [0] * FRACTION_BITS
        return [sign] + exponent_bits + rounded_bits

    @staticmethod
    def to_decimal(bits):
        sign = -1 if bits[0] == 1 else 1
        exponent_raw = BitArray32.to_unsigned_int(bits[1:9])
        fraction_bits = bits[9:]
        fraction_value = Decimal(0)
        step = Decimal('0.5')
        for bit in fraction_bits:
            if bit:
                fraction_value += step
            step /= 2
        if exponent_raw == 0:
            if fraction_value == 0:
                return Decimal(0)
            exponent = MIN_NORMAL_EXP
            mantissa = fraction_value
        elif exponent_raw == 255:
            raise ValueError('Infinity and NaN are not supported in decimal conversion')
        else:
            exponent = exponent_raw - BIAS
            mantissa = Decimal(1) + fraction_value
        return Decimal(sign) * mantissa * (Decimal(2) ** exponent)

    @staticmethod
    def _negate(bits):
        if BitArray32.is_zero(bits[1:]):
            return bits[:]
        return [1 - bits[0]] + bits[1:]

    @staticmethod
    def add_bits(a_bits, b_bits):
        a_sign, a_exp, a_mant = IEEE754Binary32._unpack(a_bits)
        b_sign, b_exp, b_mant = IEEE754Binary32._unpack(b_bits)

        if a_mant == 0:
            return b_bits[:]
        if b_mant == 0:
            return a_bits[:]

        extra_bits = 3
        a_mant <<= extra_bits
        b_mant <<= extra_bits

        common_exp = a_exp
        if a_exp > b_exp:
            b_mant = IEEE754Binary32._shift_right_with_sticky(b_mant, a_exp - b_exp)
        elif b_exp > a_exp:
            a_mant = IEEE754Binary32._shift_right_with_sticky(a_mant, b_exp - a_exp)
            common_exp = b_exp

        if a_sign == b_sign:
            result_sign = a_sign
            result_mant = a_mant + b_mant
        else:
            if a_mant > b_mant:
                result_sign = a_sign
                result_mant = a_mant - b_mant
            elif b_mant > a_mant:
                result_sign = b_sign
                result_mant = b_mant - a_mant
            else:
                return [0] * 32

        return IEEE754Binary32._pack(result_sign, result_mant, common_exp, FRACTION_BITS + extra_bits)

    @staticmethod
    def subtract_bits(a_bits, b_bits):
        return IEEE754Binary32.add_bits(a_bits, IEEE754Binary32._negate(b_bits))

    @staticmethod
    def multiply_bits(a_bits, b_bits):
        a_sign, a_exp, a_mant = IEEE754Binary32._unpack(a_bits)
        b_sign, b_exp, b_mant = IEEE754Binary32._unpack(b_bits)
        if a_mant == 0 or b_mant == 0:
            return [0] * 32
        result_sign = a_sign ^ b_sign
        result_mant = a_mant * b_mant
        result_exp = a_exp + b_exp
        return IEEE754Binary32._pack(result_sign, result_mant, result_exp, FRACTION_BITS * 2)

    @staticmethod
    def divide_bits(a_bits, b_bits):
        a_sign, a_exp, a_mant = IEEE754Binary32._unpack(a_bits)
        b_sign, b_exp, b_mant = IEEE754Binary32._unpack(b_bits)
        if b_mant == 0:
            raise ZeroDivisionError('Division by zero')
        if a_mant == 0:
            return [0] * 32
        result_sign = a_sign ^ b_sign
        precision = 64
        quotient = (a_mant << precision) // b_mant
        remainder = (a_mant << precision) % b_mant
        if remainder != 0:
            quotient |= 1
        result_exp = a_exp - b_exp
        return IEEE754Binary32._pack(result_sign, quotient, result_exp, precision)

    @staticmethod
    def add(a, b):
        a_bits = IEEE754Binary32.from_decimal(a)
        b_bits = IEEE754Binary32.from_decimal(b)
        result_bits = IEEE754Binary32.add_bits(a_bits, b_bits)
        return {
            'a_bits': a_bits,
            'b_bits': b_bits,
            'result_bits': result_bits,
            'result_value': IEEE754Binary32.to_decimal(result_bits),
        }

    @staticmethod
    def subtract(a, b):
        a_bits = IEEE754Binary32.from_decimal(a)
        b_bits = IEEE754Binary32.from_decimal(b)
        result_bits = IEEE754Binary32.subtract_bits(a_bits, b_bits)
        return {
            'a_bits': a_bits,
            'b_bits': b_bits,
            'result_bits': result_bits,
            'result_value': IEEE754Binary32.to_decimal(result_bits),
        }

    @staticmethod
    def multiply(a, b):
        a_bits = IEEE754Binary32.from_decimal(a)
        b_bits = IEEE754Binary32.from_decimal(b)
        result_bits = IEEE754Binary32.multiply_bits(a_bits, b_bits)
        return {
            'a_bits': a_bits,
            'b_bits': b_bits,
            'result_bits': result_bits,
            'result_value': IEEE754Binary32.to_decimal(result_bits),
        }

    @staticmethod
    def divide(a, b):
        a_bits = IEEE754Binary32.from_decimal(a)
        b_bits = IEEE754Binary32.from_decimal(b)
        result_bits = IEEE754Binary32.divide_bits(a_bits, b_bits)
        return {
            'a_bits': a_bits,
            'b_bits': b_bits,
            'result_bits': result_bits,
            'result_value': IEEE754Binary32.to_decimal(result_bits),
        }