from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class TruthTableRow:
    index: int
    values: Dict[str, int]
    expression_values: Dict[str, int]
    result: int


@dataclass(frozen=True)
class TruthTable:
    variables: List[str]
    expressions: List[str]
    rows: List[TruthTableRow]

    def results_vector(self) -> List[int]:
        return [row.result for row in self.rows]


@dataclass(frozen=True)
class NumericForms:
    sdnf_indices: List[int]
    sknf_indices: List[int]
    index_form: int


@dataclass(frozen=True)
class PostClassesResult:
    t0: bool
    t1: bool
    s: bool
    m: bool
    l: bool


@dataclass(frozen=True)
class ZhegalkinTerm:
    variables: List[str]

    def is_constant_one(self) -> bool:
        return len(self.variables) == 0


@dataclass(frozen=True)
class DerivativeResult:
    by_variables: List[str]
    truth_table: TruthTable
    expression: str


@dataclass(frozen=True)
class Implicant:
    pattern: str
    covered_indices: List[int]

    def rank(self) -> int:
        return self.pattern.count("0") + self.pattern.count("1")


@dataclass(frozen=True)
class GluingStep:
    source_patterns: List[str]
    result_patterns: List[str]


@dataclass(frozen=True)
class MinimizationResult:
    original_expression: str
    gluing_steps: List[GluingStep]
    prime_implicants: List[Implicant]
    essential_implicants: List[Implicant]
    redundant_implicants: List[Implicant]
    minimized_expression: str
    coverage_table: List[List[int]]


@dataclass(frozen=True)
class KarnaughGroup:
    cells: List[int]
    pattern: str
    expression: str


@dataclass(frozen=True)
class KarnaughResult:
    map_rows: List[List[int]]
    groups: List[KarnaughGroup]
    minimized_expression: str


@dataclass(frozen=True)
class AnalysisResult:
    expression: str
    variables: List[str]
    truth_table: TruthTable
    sdnf: str
    sknf: str
    numeric_forms: NumericForms
    post_classes: PostClassesResult
    zhegalkin_polynomial: str
    fictive_variables: List[str]
    derivatives: List[DerivativeResult]
    calculation_minimization: MinimizationResult
    calculation_table_minimization: MinimizationResult
    karnaugh_minimization: KarnaughResult