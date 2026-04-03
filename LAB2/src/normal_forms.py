from models import NumericForms, TruthTable


def build_sdnf_terms(table: TruthTable) -> list[str]:
    terms: list[str] = []

    for row in table.rows:
        if row.result != 1:
            continue

        parts: list[str] = []
        for variable in table.variables:
            value = row.values[variable]
            parts.append(variable if value == 1 else f"!{variable}")

        if len(parts) == 1:
            terms.append(parts[0])
        else:
            terms.append("(" + "&".join(parts) + ")")

    return terms


def build_sknf_terms(table: TruthTable) -> list[str]:
    terms: list[str] = []

    for row in table.rows:
        if row.result != 0:
            continue

        parts: list[str] = []
        for variable in table.variables:
            value = row.values[variable]
            parts.append(variable if value == 0 else f"!{variable}")

        if len(parts) == 1:
            terms.append(parts[0])
        else:
            terms.append("(" + "|".join(parts) + ")")

    return terms


def build_sdnf(table: TruthTable) -> str:
    terms = build_sdnf_terms(table)
    if len(terms) == 0:
        return "0"
    return "|".join(terms)


def build_sknf(table: TruthTable) -> str:
    terms = build_sknf_terms(table)
    if len(terms) == 0:
        return "1"
    return "&".join(terms)


def build_index_form(table: TruthTable) -> int:
    value = 0
    for result in table.results_vector():
        value = value * 2 + result
    return value


def build_numeric_forms(table: TruthTable) -> NumericForms:
    sdnf_indices = [row.index for row in table.rows if row.result == 1]
    sknf_indices = [row.index for row in table.rows if row.result == 0]
    index_form = build_index_form(table)
    return NumericForms(
        sdnf_indices=sdnf_indices,
        sknf_indices=sknf_indices,
        index_form=index_form,
    )