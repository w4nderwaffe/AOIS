from .bit_array import BIT_WIDTH, BitArray32

MAX_MAGNITUDE = (1 << (BIT_WIDTH - 1)) - 1
MIN_VALUE = -(1 << (BIT_WIDTH - 1))
MAX_VALUE = (1 << (BIT_WIDTH - 1)) - 1


class IntegerCodes:
    @staticmethod
    def _check_sign_magnitude_range(value: int):
        if abs(value) > MAX_MAGNITUDE:
            raise OverflowError('Magnitude does not fit into sign-magnitude code')

    @staticmethod
    def _check_twos_complement_range(value: int):
        if value < MIN_VALUE or value > MAX_VALUE:
            raise OverflowError('Value does not fit into 32-bit two\'s complement')

    @staticmethod
    def to_sign_magnitude(value: int):
        IntegerCodes._check_sign_magnitude_range(value)
        sign = 1 if value < 0 else 0
        magnitude_bits = BitArray32.from_unsigned_int(abs(value), BIT_WIDTH - 1)
        return [sign] + magnitude_bits

    @staticmethod
    def to_ones_complement(value: int):
        IntegerCodes._check_sign_magnitude_range(value)
        if value >= 0:
            return [0] + BitArray32.from_unsigned_int(value, BIT_WIDTH - 1)
        positive = [0] + BitArray32.from_unsigned_int(abs(value), BIT_WIDTH - 1)
        return BitArray32.invert(positive)

    @staticmethod
    def to_twos_complement(value: int):
        IntegerCodes._check_twos_complement_range(value)
        if value >= 0:
            return BitArray32.from_unsigned_int(value, BIT_WIDTH)
        magnitude = BitArray32.from_unsigned_int(abs(value), BIT_WIDTH)
        inverted = BitArray32.invert(magnitude)
        return BitArray32.add_one(inverted)

    @staticmethod
    def from_sign_magnitude(bits):
        if len(bits) != BIT_WIDTH:
            raise ValueError('Bit array must contain 32 bits')
        sign = bits[0]
        magnitude = BitArray32.to_unsigned_int(bits[1:])
        return -magnitude if sign else magnitude

    @staticmethod
    def from_ones_complement(bits):
        if len(bits) != BIT_WIDTH:
            raise ValueError('Bit array must contain 32 bits')
        if bits[0] == 0:
            return BitArray32.to_unsigned_int(bits[1:])
        restored = BitArray32.invert(bits)
        magnitude = BitArray32.to_unsigned_int(restored[1:])
        return -magnitude

    @staticmethod
    def from_twos_complement(bits):
        if len(bits) != BIT_WIDTH:
            raise ValueError('Bit array must contain 32 bits')
        if bits[0] == 0:
            return BitArray32.to_unsigned_int(bits)
        inverted = BitArray32.invert(bits)
        magnitude_bits = BitArray32.add_one(inverted)
        magnitude = BitArray32.to_unsigned_int(magnitude_bits)
        return -magnitude

    @staticmethod
    def add(a_value: int, b_value: int):
        a_bits = IntegerCodes.to_twos_complement(a_value)
        b_bits = IntegerCodes.to_twos_complement(b_value)
        result_bits, _ = BitArray32.add_bits(a_bits, b_bits)
        result_value = IntegerCodes.from_twos_complement(result_bits)

        if (a_value >= 0 and b_value >= 0 and result_value < 0) or (
            a_value < 0 and b_value < 0 and result_value >= 0
        ):
            raise OverflowError('Addition overflow in two\'s complement')

        return {
            'a_bits': a_bits,
            'b_bits': b_bits,
            'result_bits': result_bits,
            'result_value': result_value,
        }

    @staticmethod
    def subtract(a_value: int, b_value: int):
        if b_value == MIN_VALUE:
            raise OverflowError('Subtraction overflow')
        negative_b = -b_value
        a_bits = IntegerCodes.to_twos_complement(a_value)
        b_bits = IntegerCodes.to_twos_complement(b_value)
        result = IntegerCodes.add(a_value, negative_b)
        return {
            'a_bits': a_bits,
            'b_bits': b_bits,
            'result_bits': result['result_bits'],
            'result_value': result['result_value'],
        }