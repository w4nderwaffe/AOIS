from decimal import Decimal, getcontext

from .bit_array import BIT_WIDTH, BitArray32
from .integer_codes import IntegerCodes, MAX_MAGNITUDE

getcontext().prec = 80


class DirectCodeArithmetic:
    @staticmethod
    def _unsigned_add(a_bits, b_bits):
        return BitArray32.add_bits(a_bits, b_bits)

    @staticmethod
    def _unsigned_subtract(a_bits, b_bits):
        if BitArray32.compare_unsigned(a_bits, b_bits) < 0:
            raise ValueError('Unsigned subtraction requires a >= b')
        inverted = BitArray32.invert(b_bits)
        plus_one = BitArray32.add_one(inverted)
        result, _ = BitArray32.add_bits(a_bits, plus_one)
        return result

    @staticmethod
    def multiply(a_value: int, b_value: int):
        if abs(a_value) > MAX_MAGNITUDE or abs(b_value) > MAX_MAGNITUDE:
            raise OverflowError('Magnitude does not fit into direct code')
        sign = 1 if (a_value < 0) ^ (b_value < 0) else 0
        multiplicand_bits = BitArray32.from_unsigned_int(abs(a_value), BIT_WIDTH - 1)
        multiplier_bits = BitArray32.from_unsigned_int(abs(b_value), BIT_WIDTH - 1)
        product_bits = [0] * (BIT_WIDTH - 1)

        for index in range(BIT_WIDTH - 2, -1, -1):
            if multiplier_bits[index] == 1:
                shift = (BIT_WIDTH - 2) - index
                if shift > 0 and any(multiplicand_bits[:shift]):
                    raise OverflowError('Multiplication overflow in direct code')
                shifted = BitArray32.shift_left(multiplicand_bits, shift)
                product_bits, carry = BitArray32.add_bits(product_bits, shifted)
                if carry:
                    raise OverflowError('Multiplication overflow in direct code')

        product = BitArray32.to_unsigned_int(product_bits)
        bits = [sign] + product_bits
        return {
            'a_bits': IntegerCodes.to_sign_magnitude(a_value),
            'b_bits': IntegerCodes.to_sign_magnitude(b_value),
            'result_bits': bits,
            'result_value': -product if sign else product,
        }

    @staticmethod
    def divide(a_value: int, b_value: int, precision: int = 5):
        if b_value == 0:
            raise ZeroDivisionError('Division by zero')
        sign = -1 if (a_value < 0) ^ (b_value < 0) else 1
        numerator = abs(a_value)
        denominator = abs(b_value)

        integer_part = numerator // denominator
        remainder = numerator % denominator
        if integer_part > MAX_MAGNITUDE:
            raise OverflowError('Division result integer part does not fit into direct code')

        digits = []
        scaled_abs = integer_part
        for _ in range(precision):
            remainder *= 10
            digit = remainder // denominator
            remainder %= denominator
            digits.append(str(digit))
            scaled_abs = scaled_abs * 10 + digit

        if scaled_abs > MAX_MAGNITUDE:
            raise OverflowError('Scaled division result does not fit into direct code')

        decimal_text = f"{integer_part}." + ''.join(digits)
        decimal_value = Decimal(decimal_text)
        if sign < 0:
            decimal_value = -decimal_value

        bits = IntegerCodes.to_sign_magnitude(scaled_abs if sign > 0 else -scaled_abs)
        return {
            'a_bits': IntegerCodes.to_sign_magnitude(a_value),
            'b_bits': IntegerCodes.to_sign_magnitude(b_value),
            'result_bits': bits,
            'result_value': decimal_value,
            'scaled_integer': scaled_abs if sign > 0 else -scaled_abs,
        }