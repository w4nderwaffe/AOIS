BIT_WIDTH = 32


class BitArray32:
    @staticmethod
    def zero():
        return [0] * BIT_WIDTH

    @staticmethod
    def from_unsigned_int(value: int, size: int = BIT_WIDTH):
        if value < 0:
            raise ValueError('Unsigned value must be non-negative')
        bits = [0] * size
        for i in range(size - 1, -1, -1):
            bits[i] = value % 2
            value //= 2
        if value != 0:
            raise OverflowError('Value does not fit into the requested size')
        return bits

    @staticmethod
    def to_unsigned_int(bits):
        value = 0
        for bit in bits:
            value = value * 2 + bit
        return value

    @staticmethod
    def to_string(bits):
        return ''.join(str(bit) for bit in bits)

    @staticmethod
    def invert(bits):
        return [1 - bit for bit in bits]

    @staticmethod
    def add_bits(a, b):
        if len(a) != len(b):
            raise ValueError('Bit arrays must have equal length')
        result = [0] * len(a)
        carry = 0
        for i in range(len(a) - 1, -1, -1):
            total = a[i] + b[i] + carry
            result[i] = total % 2
            carry = total // 2
        return result, carry

    @staticmethod
    def add_one(bits):
        one = [0] * len(bits)
        one[-1] = 1
        result, _ = BitArray32.add_bits(bits, one)
        return result

    @staticmethod
    def compare_unsigned(a, b):
        if len(a) != len(b):
            raise ValueError('Bit arrays must have equal length')
        for left, right in zip(a, b):
            if left < right:
                return -1
            if left > right:
                return 1
        return 0

    @staticmethod
    def shift_left(bits, count=1):
        if count < 0:
            raise ValueError('Shift count must be non-negative')
        if count >= len(bits):
            return [0] * len(bits)
        return bits[count:] + [0] * count

    @staticmethod
    def shift_right_logical(bits, count=1):
        if count < 0:
            raise ValueError('Shift count must be non-negative')
        if count >= len(bits):
            return [0] * len(bits)
        return [0] * count + bits[:len(bits) - count]

    @staticmethod
    def is_zero(bits):
        for bit in bits:
            if bit != 0:
                return False
        return True
