from models import (
    AnalysisResult,
    DerivativeResult,
    KarnaughResult,
    MinimizationResult,
    NumericForms,
    PostClassesResult,
    TruthTable,
)


def _build_aligned_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]

    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    def format_row(items: list[str]) -> str:
        return " | ".join(item.ljust(widths[index]) for index, item in enumerate(items))

    separator = "-+-".join("-" * width for width in widths)

    lines = [format_row(headers), separator]
    for row in rows:
        lines.append(format_row(row))

    return "\n".join(lines)


def format_truth_table(table: TruthTable) -> str:
    headers = table.variables + table.expressions
    lines = ["Таблица истинности:"]

    if len(headers) == 0:
        lines.append("-")
        return "\n".join(lines)

    rows: list[list[str]] = []
    for row in table.rows:
        values = [str(row.values[variable]) for variable in table.variables]
        expressions = [str(row.expression_values[expression]) for expression in table.expressions]
        rows.append(values + expressions)

    lines.append(_build_aligned_table(headers, rows))
    return "\n".join(lines)


def format_numeric_forms(forms: NumericForms) -> str:
    sdnf_indices = ", ".join(str(value) for value in forms.sdnf_indices)
    sknf_indices = ", ".join(str(value) for value in forms.sknf_indices)

    return "\n".join(
        [
            "Числовые формы:",
            f"СДНФ: Σ({sdnf_indices})" if len(forms.sdnf_indices) > 0 else "СДНФ: Σ()",
            f"СКНФ: Π({sknf_indices})" if len(forms.sknf_indices) > 0 else "СКНФ: Π()",
            f"Индексная форма: {forms.index_form}",
        ]
    )


def format_post_classes(result: PostClassesResult) -> str:
    lines = [
        "Классы Поста:",
        f"T0: {'Да' if result.t0 else 'Нет'}",
        f"T1: {'Да' if result.t1 else 'Нет'}",
        f"S : {'Да' if result.s else 'Нет'}",
        f"M : {'Да' if result.m else 'Нет'}",
        f"L : {'Да' if result.l else 'Нет'}",
    ]
    return "\n".join(lines)


def format_derivative(result: DerivativeResult) -> str:
    variables = ", ".join(result.by_variables)
    lines = [
        f"Производная по переменным: {variables}",
        format_truth_table(result.truth_table),
        f"Выражение: {result.expression}",
    ]
    return "\n".join(lines)


def _format_gluing_steps(result: MinimizationResult) -> list[str]:
    if len(result.gluing_steps) == 0:
        return ["Этапы склеивания: отсутствуют"]

    lines = ["Этапы склеивания:"]
    for index, step in enumerate(result.gluing_steps, start=1):
        lines.append(f"Шаг {index}:")
        if len(step.source_patterns) == 0:
            lines.append("  Исходные шаблоны: -")
        else:
            lines.append("  Исходные шаблоны:")
            for item in step.source_patterns:
                lines.append(f"    {item}")

        if len(step.result_patterns) == 0:
            lines.append("  Результаты: -")
        else:
            lines.append("  Результаты:")
            for item in step.result_patterns:
                lines.append(f"    {item}")

    return lines


def _format_implicants(title: str, items) -> list[str]:
    lines = [title]
    if len(items) == 0:
        lines.append("  -")
        return lines

    for item in items:
        covered = ", ".join(str(value) for value in item.covered_indices)
        lines.append(f"  {item.pattern} -> [{covered}]")

    return lines


def _format_coverage_table(table_data: list[list[int]]) -> list[str]:
    lines = ["Таблица покрытия:"]
    if len(table_data) == 0:
        lines.append("  -")
        return lines

    rows = [[str(value) for value in row] for row in table_data]
    headers = [str(index + 1) for index in range(len(rows[0]))]
    lines.append(_build_aligned_table(headers, rows))
    return lines


def format_minimization_result(result: MinimizationResult) -> str:
    lines = [
        "Результат минимизации:",
        f"Исходное выражение: {result.original_expression}",
    ]

    lines.extend(_format_gluing_steps(result))
    lines.extend(_format_implicants("Простые импликанты:", result.prime_implicants))
    lines.extend(_format_implicants("Выбранные импликанты:", result.essential_implicants))
    lines.extend(_format_implicants("Лишние импликанты:", result.redundant_implicants))
    lines.extend(_format_coverage_table(result.coverage_table))
    lines.append(f"Минимизированное выражение: {result.minimized_expression}")

    return "\n".join(lines)


def format_karnaugh_result(result: KarnaughResult) -> str:
    lines = ["Карта Карно:"]

    if len(result.map_rows) == 0:
        lines.append("  -")
    else:
        rows = [[str(value) for value in row] for row in result.map_rows]
        headers = [str(index + 1) for index in range(len(rows[0]))]
        lines.append(_build_aligned_table(headers, rows))

    lines.append("Группы:")
    if len(result.groups) == 0:
        lines.append("  -")
    else:
        for group in result.groups:
            cells = ", ".join(str(value) for value in group.cells)
            lines.append(
                f"  cells=[{cells}] pattern={group.pattern} expression={group.expression}"
            )

    lines.append(f"Минимизированное выражение: {result.minimized_expression}")
    return "\n".join(lines)


def format_analysis_result(result: AnalysisResult) -> str:
    lines = [
        "Результат анализа логической функции",
        f"Исходное выражение: {result.expression}",
        f"Переменные: {', '.join(result.variables)}",
        "",
        format_truth_table(result.truth_table),
        "",
        f"СДНФ: {result.sdnf}",
        f"СКНФ: {result.sknf}",
        "",
        format_numeric_forms(result.numeric_forms),
        "",
        format_post_classes(result.post_classes),
        "",
        f"Полином Жегалкина: {result.zhegalkin_polynomial}",
        f"Фиктивные переменные: {', '.join(result.fictive_variables) if len(result.fictive_variables) > 0 else '-'}",
        "",
        "Булевы производные:",
    ]

    if len(result.derivatives) == 0:
        lines.append("-")
    else:
        for derivative in result.derivatives:
            lines.append(format_derivative(derivative))
            lines.append("")

    lines.append("Минимизация расчетным методом:")
    lines.append(format_minimization_result(result.calculation_minimization))
    lines.append("")
    lines.append("Минимизация расчетно-табличным методом:")
    lines.append(format_minimization_result(result.calculation_table_minimization))
    lines.append("")
    lines.append("Минимизация табличным методом (карта Карно):")
    lines.append(format_karnaugh_result(result.karnaugh_minimization))

    return "\n".join(lines)