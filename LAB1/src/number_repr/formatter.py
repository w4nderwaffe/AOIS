from decimal import Decimal

from .bit_array import BitArray32


class Formatter:
    @staticmethod
    def bits(bits):
        return BitArray32.to_string(bits)

    @staticmethod
    def decimal(value):
        if isinstance(value, Decimal):
            text = format(value, 'f')
            if '.' in text:
                text = text.rstrip('0').rstrip('.') or '0'
            return text
        return str(value)

    @staticmethod
    def report(binary_value, decimal_value):
        return {
            'binary': Formatter.bits(binary_value),
            'decimal': Formatter.decimal(decimal_value),
        }
