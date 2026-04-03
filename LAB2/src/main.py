from app import LogicFunctionAnalyzer
from formatter import (
    format_derivative,
    format_karnaugh_result,
    format_minimization_result,
    format_numeric_forms,
    format_post_classes,
    format_truth_table,
)


def read_expression() -> str:
    while True:
        expression = input("Введите логическую функцию: ").strip()
        if len(expression) > 0:
            return expression
        print("Функция не должна быть пустой.")


def print_menu() -> None:
    print("\nВыберите действие:")
    print("1. Ввести новую функцию")
    print("2. Показать таблицу истинности")
    print("3. Показать СДНФ")
    print("4. Показать СКНФ")
    print("5. Показать числовые формы и индексную форму")
    print("6. Показать принадлежность к классам Поста")
    print("7. Показать полином Жегалкина")
    print("8. Показать фиктивные переменные")
    print("9. Показать булевы производные")
    print("10. Минимизация расчетным методом")
    print("11. Минимизация расчетно-табличным методом")
    print("12. Минимизация табличным методом (карта Карно)")
    print("13. Показать полный анализ")
    print("0. Выход")


def choose_derivative(result) -> None:
    if len(result.derivatives) == 0:
        print("Производные отсутствуют.")
        return

    print("\nДоступные производные:")
    for index, derivative in enumerate(result.derivatives, start=1):
        variables = ", ".join(derivative.by_variables)
        print(f"{index}. По переменным: {variables}")

    while True:
        raw_value = input("Введите номер производной (0 - назад): ").strip()

        if raw_value == "0":
            return

        try:
            number = int(raw_value)
        except ValueError:
            print("Введите корректный номер.")
            continue

        if 1 <= number <= len(result.derivatives):
            print()
            print(format_derivative(result.derivatives[number - 1]))
            return

        print("Такого номера нет.")


def print_full_analysis(result) -> None:
    print()
    print("Исходное выражение:", result.expression)
    print("Переменные:", ", ".join(result.variables))
    print()
    print(format_truth_table(result.truth_table))
    print()
    print("СДНФ:", result.sdnf)
    print("СКНФ:", result.sknf)
    print()
    print(format_numeric_forms(result.numeric_forms))
    print()
    print(format_post_classes(result.post_classes))
    print()
    print("Полином Жегалкина:", result.zhegalkin_polynomial)
    print(
        "Фиктивные переменные:",
        ", ".join(result.fictive_variables) if len(result.fictive_variables) > 0 else "-",
    )
    print()
    print("Минимизация расчетным методом:")
    print(format_minimization_result(result.calculation_minimization))
    print()
    print("Минимизация расчетно-табличным методом:")
    print(format_minimization_result(result.calculation_table_minimization))
    print()
    print("Минимизация табличным методом (карта Карно):")
    print(format_karnaugh_result(result.karnaugh_minimization))


def main() -> None:
    analyzer = LogicFunctionAnalyzer()

    current_expression = None
    current_result = None

    while True:
        if current_result is None:
            try:
                current_expression = read_expression()
                current_result = analyzer.analyze(current_expression)
                print("\nФункция успешно разобрана.")
            except Exception as error:
                print(f"Ошибка: {error}")
                continue

        print_menu()
        choice = input("Введите номер действия: ").strip()

        if choice == "0":
            print("Завершение программы.")
            break

        if choice == "1":
            try:
                current_expression = read_expression()
                current_result = analyzer.analyze(current_expression)
                print("\nФункция успешно разобрана.")
            except Exception as error:
                print(f"Ошибка: {error}")
                current_result = None
            continue

        if choice == "2":
            print()
            print(format_truth_table(current_result.truth_table))
            continue

        if choice == "3":
            print()
            print("СДНФ:", current_result.sdnf)
            continue

        if choice == "4":
            print()
            print("СКНФ:", current_result.sknf)
            continue

        if choice == "5":
            print()
            print(format_numeric_forms(current_result.numeric_forms))
            continue

        if choice == "6":
            print()
            print(format_post_classes(current_result.post_classes))
            continue

        if choice == "7":
            print()
            print("Полином Жегалкина:", current_result.zhegalkin_polynomial)
            continue

        if choice == "8":
            print()
            if len(current_result.fictive_variables) == 0:
                print("Фиктивные переменные: -")
            else:
                print("Фиктивные переменные:", ", ".join(current_result.fictive_variables))
            continue

        if choice == "9":
            choose_derivative(current_result)
            continue

        if choice == "10":
            print()
            print("Минимизация расчетным методом:")
            print(format_minimization_result(current_result.calculation_minimization))
            continue

        if choice == "11":
            print()
            print("Минимизация расчетно-табличным методом:")
            print(format_minimization_result(current_result.calculation_table_minimization))
            continue

        if choice == "12":
            print()
            print("Минимизация табличным методом (карта Карно):")
            print(format_karnaugh_result(current_result.karnaugh_minimization))
            continue

        if choice == "13":
            print_full_analysis(current_result)
            continue

        print("Некорректный пункт меню.")


if __name__ == "__main__":
    main()