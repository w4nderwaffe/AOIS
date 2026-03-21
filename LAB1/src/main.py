from number_repr import BCD2421, Formatter, IEEE754Binary32, IntegerCodes, DirectCodeArithmetic


def read_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print('Введите целое число.')


def read_float(prompt):
    while True:
        value = input(prompt).strip().replace(',', '.')
        try:
            return float(value)
        except ValueError:
            print('Введите число.')


def print_integer_codes(value):
    print(f'\nКоды числа {value}:')
    print('Прямой код        :', Formatter.bits(IntegerCodes.to_sign_magnitude(value)))
    print('Обратный код      :', Formatter.bits(IntegerCodes.to_ones_complement(value)))
    print('Дополнительный код:', Formatter.bits(IntegerCodes.to_twos_complement(value)))


def print_integer_operations(a, b):
    print(f'\nОперации для целых чисел {a} и {b}:')

    add_result = IntegerCodes.add(a, b)
    print('Сложение (доп. код):')
    print('  A      =', Formatter.bits(add_result['a_bits']))
    print('  B      =', Formatter.bits(add_result['b_bits']))
    print('  Result =', Formatter.bits(add_result['result_bits']))
    print('  Decimal=', add_result['result_value'])

    sub_result = IntegerCodes.subtract(a, b)
    print('Вычитание (доп. код):')
    print('  A      =', Formatter.bits(sub_result['a_bits']))
    print('  B      =', Formatter.bits(sub_result['b_bits']))
    print('  Result =', Formatter.bits(sub_result['result_bits']))
    print('  Decimal=', sub_result['result_value'])

    mul_result = DirectCodeArithmetic.multiply(a, b)
    print('Умножение (прямой код):')
    print('  A      =', Formatter.bits(mul_result['a_bits']))
    print('  B      =', Formatter.bits(mul_result['b_bits']))
    print('  Result =', Formatter.bits(mul_result['result_bits']))
    print('  Decimal=', mul_result['result_value'])

    try:
        div_result = DirectCodeArithmetic.divide(a, b)
        print('Деление (прямой код):')
        print('  A      =', Formatter.bits(div_result['a_bits']))
        print('  B      =', Formatter.bits(div_result['b_bits']))
        print('  Result =', Formatter.bits(div_result['result_bits']))
        print('  Decimal=', Formatter.decimal(div_result['result_value']))
    except ZeroDivisionError:
        print('Деление (прямой код): деление на ноль невозможно')


def print_float_operations(a, b):
    print(f'\nIEEE-754 операции для чисел {a} и {b}:')

    add_result = IEEE754Binary32.add(a, b)
    print('IEEE-754 сложение:')
    print('  A      =', Formatter.bits(add_result['a_bits']))
    print('  B      =', Formatter.bits(add_result['b_bits']))
    print('  Result =', Formatter.bits(add_result['result_bits']))
    print('  Decimal=', Formatter.decimal(add_result['result_value']))

    sub_result = IEEE754Binary32.subtract(a, b)
    print('IEEE-754 вычитание:')
    print('  A      =', Formatter.bits(sub_result['a_bits']))
    print('  B      =', Formatter.bits(sub_result['b_bits']))
    print('  Result =', Formatter.bits(sub_result['result_bits']))
    print('  Decimal=', Formatter.decimal(sub_result['result_value']))

    mul_result = IEEE754Binary32.multiply(a, b)
    print('IEEE-754 умножение:')
    print('  A      =', Formatter.bits(mul_result['a_bits']))
    print('  B      =', Formatter.bits(mul_result['b_bits']))
    print('  Result =', Formatter.bits(mul_result['result_bits']))
    print('  Decimal=', Formatter.decimal(mul_result['result_value']))

    try:
        div_result = IEEE754Binary32.divide(a, b)
        print('IEEE-754 деление:')
        print('  A      =', Formatter.bits(div_result['a_bits']))
        print('  B      =', Formatter.bits(div_result['b_bits']))
        print('  Result =', Formatter.bits(div_result['result_bits']))
        print('  Decimal=', Formatter.decimal(div_result['result_value']))
    except ZeroDivisionError:
        print('IEEE-754 деление: деление на ноль невозможно')


def print_bcd_operation(a, b):
    print(f'\nBCD 2421 для чисел {a} и {b}:')
    try:
        result = BCD2421.add(a, b)
        print('BCD 2421 сложение:')
        print('  A      =', Formatter.bits(result['a_bits']))
        print('  B      =', Formatter.bits(result['b_bits']))
        print('  Result =', Formatter.bits(result['result_bits']))
        print('  Decimal=', result['result_value'])
    except ValueError as error:
        print('BCD 2421 сложение:', error)


def main():
    print('Лабораторная работа №1')
    print('Введите данные для демонстрации операций.')

    integer_a = read_int('\nВведите первое целое число: ')
    integer_b = read_int('Введите второе целое число: ')

    float_a = read_float('\nВведите первое вещественное число: ')
    float_b = read_float('Введите второе вещественное число: ')

    bcd_a = read_int('\nВведите первое неотрицательное число для BCD 2421: ')
    bcd_b = read_int('Введите второе неотрицательное число для BCD 2421: ')

    print_integer_codes(integer_a)
    print_integer_codes(integer_b)
    print_integer_operations(integer_a, integer_b)
    print_float_operations(float_a, float_b)
    print_bcd_operation(bcd_a, bcd_b)


if __name__ == '__main__':
    main()