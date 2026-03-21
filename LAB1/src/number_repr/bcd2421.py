MAPPING = {
    0: [0, 0, 0, 0],
    1: [0, 0, 0, 1],
    2: [0, 0, 1, 0],
    3: [0, 0, 1, 1],
    4: [0, 1, 0, 0],
    5: [1, 0, 1, 1],
    6: [1, 1, 0, 0],
    7: [1, 1, 0, 1],
    8: [1, 1, 1, 0],
    9: [1, 1, 1, 1],
}
REVERSE_MAPPING = {tuple(bits): digit for digit, bits in MAPPING.items()}


class BCD2421:
    @staticmethod
    def encode_digit(digit: int):
        if digit not in MAPPING:
            raise ValueError('A decimal digit must be between 0 and 9')
        return MAPPING[digit][:]

    @staticmethod
    def decode_digit(bits):
        key = tuple(bits)
        if key not in REVERSE_MAPPING:
            raise ValueError('Invalid 2421 digit')
        return REVERSE_MAPPING[key]

    @staticmethod
    def _split_tetrads(bits):
        if len(bits) % 4 != 0:
            raise ValueError('BCD bit count must be divisible by 4')
        tetrads = []
        for i in range(0, len(bits), 4):
            tetrads.append(bits[i:i + 4])
        return tetrads

    @staticmethod
    def encode_number(value: int):
        if value < 0:
            raise ValueError('BCD only supports non-negative integers')
        digits = [int(ch) for ch in str(value)]
        result = []
        for digit in digits:
            result.extend(BCD2421.encode_digit(digit))
        return result

    @staticmethod
    def decode_number(bits):
        digits = []
        for tetrad in BCD2421._split_tetrads(bits):
            digits.append(str(BCD2421.decode_digit(tetrad)))
        return int(''.join(digits))

    @staticmethod
    def _add_tetrads(a_tetrad, b_tetrad, carry):
        a_digit = BCD2421.decode_digit(a_tetrad)
        b_digit = BCD2421.decode_digit(b_tetrad)
        total = a_digit + b_digit + carry
        return total % 10, total // 10

    @staticmethod
    def add(a_value: int, b_value: int):
        if a_value < 0 or b_value < 0:
            raise ValueError('BCD addition supports only non-negative integers')

        a_bits = BCD2421.encode_number(a_value)
        b_bits = BCD2421.encode_number(b_value)
        a_tetrads = BCD2421._split_tetrads(a_bits)
        b_tetrads = BCD2421._split_tetrads(b_bits)

        max_len = max(len(a_tetrads), len(b_tetrads))
        zero_tetrad = BCD2421.encode_digit(0)
        a_tetrads = [zero_tetrad[:]] * (max_len - len(a_tetrads)) + a_tetrads
        b_tetrads = [zero_tetrad[:]] * (max_len - len(b_tetrads)) + b_tetrads

        carry = 0
        result_tetrads = []
        for index in range(max_len - 1, -1, -1):
            digit, carry = BCD2421._add_tetrads(a_tetrads[index], b_tetrads[index], carry)
            result_tetrads.append(BCD2421.encode_digit(digit))

        if carry:
            result_tetrads.append(BCD2421.encode_digit(carry))

        result_tetrads.reverse()
        result_bits = []
        result_value = 0
        for tetrad in result_tetrads:
            result_bits.extend(tetrad)
            result_value = result_value * 10 + BCD2421.decode_digit(tetrad)

        return {
            'a_bits': a_bits,
            'b_bits': b_bits,
            'result_bits': result_bits,
            'result_value': result_value,
        }