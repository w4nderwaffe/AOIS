from ast_nodes import AstNode
from derivatives import build_all_required_derivatives
from fictive_variables import find_fictive_variables
from karnaugh import minimize_by_karnaugh
from lexer import Lexer
from minimization import minimize_by_calculation, minimize_by_calculation_table
from models import AnalysisResult
from normal_forms import build_numeric_forms, build_sdnf, build_sknf
from parser import Parser
from post_classes import analyze_post_classes
from truth_table import build_truth_table
from zhegalkin import build_zhegalkin_polynomial


class LogicFunctionAnalyzer:
    def analyze(self, expression: str) -> AnalysisResult:
        normalized = expression.strip()
        if len(normalized) == 0:
            raise ValueError("Пустое выражение")

        root = self._parse_expression(normalized)
        truth_table = build_truth_table(root)

        sdnf = build_sdnf(truth_table)
        sknf = build_sknf(truth_table)
        numeric_forms = build_numeric_forms(truth_table)
        post_classes = analyze_post_classes(truth_table)
        zhegalkin_polynomial = build_zhegalkin_polynomial(truth_table)
        fictive_variables = find_fictive_variables(truth_table)
        derivatives = self._build_derivatives(root, truth_table.variables)
        calculation_minimization = minimize_by_calculation(truth_table)
        calculation_table_minimization = minimize_by_calculation_table(truth_table)
        karnaugh_minimization = minimize_by_karnaugh(truth_table)

        return AnalysisResult(
            expression=normalized,
            variables=truth_table.variables,
            truth_table=truth_table,
            sdnf=sdnf,
            sknf=sknf,
            numeric_forms=numeric_forms,
            post_classes=post_classes,
            zhegalkin_polynomial=zhegalkin_polynomial,
            fictive_variables=fictive_variables,
            derivatives=derivatives,
            calculation_minimization=calculation_minimization,
            calculation_table_minimization=calculation_table_minimization,
            karnaugh_minimization=karnaugh_minimization,
        )

    def _parse_expression(self, expression: str) -> AstNode:
        tokens = Lexer(expression).tokenize()
        return Parser(tokens).parse()

    def _build_derivatives(self, root: AstNode, variables: list[str]):
        return build_all_required_derivatives(root, variables)