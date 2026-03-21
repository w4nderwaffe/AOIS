from number_repr import BCD2421, Formatter, IEEE754Binary32, IntegerCodes, DirectCodeArithmetic


def read_int(prompt):
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print('Введите целое число.')


def read_non_negative_int(prompt):
    while True:
        value = read_int(prompt)
        if value >= 0:
            return value
        print('Введите неотрицательное целое число.')


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


def run_integer_addition():
    a = read_int('\nВведите первое целое число: ')
    b = read_int('Введите второе целое число: ')
    try:
        result = IntegerCodes.add(a, b)
        print('\nСложение в дополнительном коде:')
        print('A      =', Formatter.bits(result['a_bits']))
        print('B      =', Formatter.bits(result['b_bits']))
        print('Result =', Formatter.bits(result['result_bits']))
        print('Decimal=', result['result_value'])
    except OverflowError as error:
        print('\nОшибка:', error)


def run_integer_subtraction():
    a = read_int('\nВведите уменьшаемое: ')
    b = read_int('Введите вычитаемое: ')
    try:
        result = IntegerCodes.subtract(a, b)
        print('\nВычитание в дополнительном коде:')
        print('A      =', Formatter.bits(result['a_bits']))
        print('B      =', Formatter.bits(result['b_bits']))
        print('Result =', Formatter.bits(result['result_bits']))
        print('Decimal=', result['result_value'])
    except OverflowError as error:
        print('\nОшибка:', error)


def run_integer_multiplication():
    a = read_int('\nВведите первое целое число: ')
    b = read_int('Введите второе целое число: ')
    try:
        result = DirectCodeArithmetic.multiply(a, b)
        print('\nУмножение в прямом коде:')
        print('A      =', Formatter.bits(result['a_bits']))
        print('B      =', Formatter.bits(result['b_bits']))
        print('Result =', Formatter.bits(result['result_bits']))
        print('Decimal=', result['result_value'])
    except OverflowError as error:
        print('\nОшибка:', error)


def run_integer_division():
    a = read_int('\nВведите делимое: ')
    b = read_int('Введите делитель: ')
    try:
        result = DirectCodeArithmetic.divide(a, b)
        print('\nДеление в прямом коде:')
        print('A      =', Formatter.bits(result['a_bits']))
        print('B      =', Formatter.bits(result['b_bits']))
        print('Result =', Formatter.bits(result['result_bits']))
        print('Decimal=', Formatter.decimal(result['result_value']))
    except (OverflowError, ZeroDivisionError) as error:
        print('\nОшибка:', error)


def run_float_addition():
    a = read_float('\nВведите первое вещественное число: ')
    b = read_float('Введите второе вещественное число: ')
    result = IEEE754Binary32.add(a, b)
    print('\nIEEE-754 сложение:')
    print('A      =', Formatter.bits(result['a_bits']))
    print('B      =', Formatter.bits(result['b_bits']))
    print('Result =', Formatter.bits(result['result_bits']))
    print('Decimal=', Formatter.decimal(result['result_value']))


def run_float_subtraction():
    a = read_float('\nВведите уменьшаемое: ')
    b = read_float('Введите вычитаемое: ')
    result = IEEE754Binary32.subtract(a, b)
    print('\nIEEE-754 вычитание:')
    print('A      =', Formatter.bits(result['a_bits']))
    print('B      =', Formatter.bits(result['b_bits']))
    print('Result =', Formatter.bits(result['result_bits']))
    print('Decimal=', Formatter.decimal(result['result_value']))


def run_float_multiplication():
    a = read_float('\nВведите первое вещественное число: ')
    b = read_float('Введите второе вещественное число: ')
    result = IEEE754Binary32.multiply(a, b)
    print('\nIEEE-754 умножение:')
    print('A      =', Formatter.bits(result['a_bits']))
    print('B      =', Formatter.bits(result['b_bits']))
    print('Result =', Formatter.bits(result['result_bits']))
    print('Decimal=', Formatter.decimal(result['result_value']))


def run_float_division():
    a = read_float('\nВведите делимое: ')
    b = read_float('Введите делитель: ')
    try:
        result = IEEE754Binary32.divide(a, b)
        print('\nIEEE-754 деление:')
        print('A      =', Formatter.bits(result['a_bits']))
        print('B      =', Formatter.bits(result['b_bits']))
        print('Result =', Formatter.bits(result['result_bits']))
        print('Decimal=', Formatter.decimal(result['result_value']))
    except ZeroDivisionError as error:
        print('\nОшибка:', error)


def run_bcd_addition():
    a = read_non_negative_int('\nВведите первое неотрицательное число: ')
    b = read_non_negative_int('Введите второе неотрицательное число: ')
    result = BCD2421.add(a, b)
    print('\nСложение в BCD 2421:')
    print('A      =', Formatter.bits(result['a_bits']))
    print('B      =', Formatter.bits(result['b_bits']))
    print('Result =', Formatter.bits(result['result_bits']))
    print('Decimal=', result['result_value'])


def print_menu():
    print('\nВыберите операцию:')
    print('1. Показать прямой, обратный и дополнительный коды числа')
    print('2. Сложение целых чисел в дополнительном коде')
    print('3. Вычитание целых чисел в дополнительном коде')
    print('4. Умножение целых чисел в прямом коде')
    print('5. Деление целых чисел в прямом коде')
    print('6. Сложение вещественных чисел IEEE-754')
    print('7. Вычитание вещественных чисел IEEE-754')
    print('8. Умножение вещественных чисел IEEE-754')
    print('9. Деление вещественных чисел IEEE-754')
    print('10. Сложение чисел в BCD 2421')
    print('0. Выход')


def main():
    while True:
        print_menu()
        choice = input('\nВведите номер операции: ').strip()

        if choice == '1':
            value = read_int('\nВведите целое число: ')
            print_integer_codes(value)
        elif choice == '2':
            run_integer_addition()
        elif choice == '3':
            run_integer_subtraction()
        elif choice == '4':
            run_integer_multiplication()
        elif choice == '5':
            run_integer_division()
        elif choice == '6':
            run_float_addition()
        elif choice == '7':
            run_float_subtraction()
        elif choice == '8':
            run_float_multiplication()
        elif choice == '9':
            run_float_division()
        elif choice == '10':
            run_bcd_addition()
        elif choice == '0':
            print('\nЗавершение программы.')
            break
        else:
            print('\nНекорректный пункт меню.')


if __name__ == '__main__':
    main()
