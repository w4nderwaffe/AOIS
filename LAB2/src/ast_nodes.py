from dataclasses import dataclass


class AstNode:
    def evaluate(self, values: dict[str, int]) -> int:
        raise NotImplementedError

    def collect_variables(self) -> set[str]:
        raise NotImplementedError

    def to_expression(self) -> str:
        raise NotImplementedError

    def fill_expression_values(self, values: dict[str, int], target: dict[str, int]) -> int:
        raise NotImplementedError

    def collect_subexpressions(self) -> list[str]:
        result: list[str] = []
        self._collect_subexpressions(result, set())
        return result

    def _collect_subexpressions(self, result: list[str], seen: set[str]) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class VariableNode(AstNode):
    name: str

    def evaluate(self, values: dict[str, int]) -> int:
        if self.name not in values:
            raise KeyError(f"Не задано значение переменной '{self.name}'")
        value = values[self.name]
        if value not in (0, 1):
            raise ValueError(f"Переменная '{self.name}' должна иметь значение 0 или 1")
        return value

    def collect_variables(self) -> set[str]:
        return {self.name}

    def to_expression(self) -> str:
        return self.name

    def fill_expression_values(self, values: dict[str, int], target: dict[str, int]) -> int:
        return self.evaluate(values)

    def _collect_subexpressions(self, result: list[str], seen: set[str]) -> None:
        return


@dataclass(frozen=True)
class NotNode(AstNode):
    operand: AstNode

    def evaluate(self, values: dict[str, int]) -> int:
        return 1 - self.operand.evaluate(values)

    def collect_variables(self) -> set[str]:
        return self.operand.collect_variables()

    def to_expression(self) -> str:
        operand_expression = self.operand.to_expression()
        if isinstance(self.operand, VariableNode):
            return f"!{operand_expression}"
        return f"!({operand_expression})"

    def fill_expression_values(self, values: dict[str, int], target: dict[str, int]) -> int:
        operand_value = self.operand.fill_expression_values(values, target)
        result = 1 - operand_value
        target[self.to_expression()] = result
        return result

    def _collect_subexpressions(self, result: list[str], seen: set[str]) -> None:
        self.operand._collect_subexpressions(result, seen)
        expression = self.to_expression()
        if expression not in seen:
            seen.add(expression)
            result.append(expression)


@dataclass(frozen=True)
class AndNode(AstNode):
    left: AstNode
    right: AstNode

    def evaluate(self, values: dict[str, int]) -> int:
        return self.left.evaluate(values) & self.right.evaluate(values)

    def collect_variables(self) -> set[str]:
        return self.left.collect_variables() | self.right.collect_variables()

    def to_expression(self) -> str:
        return f"({self.left.to_expression()}&{self.right.to_expression()})"

    def fill_expression_values(self, values: dict[str, int], target: dict[str, int]) -> int:
        left_value = self.left.fill_expression_values(values, target)
        right_value = self.right.fill_expression_values(values, target)
        result = left_value & right_value
        target[self.to_expression()] = result
        return result

    def _collect_subexpressions(self, result: list[str], seen: set[str]) -> None:
        self.left._collect_subexpressions(result, seen)
        self.right._collect_subexpressions(result, seen)
        expression = self.to_expression()
        if expression not in seen:
            seen.add(expression)
            result.append(expression)


@dataclass(frozen=True)
class OrNode(AstNode):
    left: AstNode
    right: AstNode

    def evaluate(self, values: dict[str, int]) -> int:
        return self.left.evaluate(values) | self.right.evaluate(values)

    def collect_variables(self) -> set[str]:
        return self.left.collect_variables() | self.right.collect_variables()

    def to_expression(self) -> str:
        return f"({self.left.to_expression()}|{self.right.to_expression()})"

    def fill_expression_values(self, values: dict[str, int], target: dict[str, int]) -> int:
        left_value = self.left.fill_expression_values(values, target)
        right_value = self.right.fill_expression_values(values, target)
        result = left_value | right_value
        target[self.to_expression()] = result
        return result

    def _collect_subexpressions(self, result: list[str], seen: set[str]) -> None:
        self.left._collect_subexpressions(result, seen)
        self.right._collect_subexpressions(result, seen)
        expression = self.to_expression()
        if expression not in seen:
            seen.add(expression)
            result.append(expression)


@dataclass(frozen=True)
class ImplNode(AstNode):
    left: AstNode
    right: AstNode

    def evaluate(self, values: dict[str, int]) -> int:
        left_value = self.left.evaluate(values)
        right_value = self.right.evaluate(values)
        return (1 - left_value) | right_value

    def collect_variables(self) -> set[str]:
        return self.left.collect_variables() | self.right.collect_variables()

    def to_expression(self) -> str:
        return f"({self.left.to_expression()}->{self.right.to_expression()})"

    def fill_expression_values(self, values: dict[str, int], target: dict[str, int]) -> int:
        left_value = self.left.fill_expression_values(values, target)
        right_value = self.right.fill_expression_values(values, target)
        result = (1 - left_value) | right_value
        target[self.to_expression()] = result
        return result

    def _collect_subexpressions(self, result: list[str], seen: set[str]) -> None:
        self.left._collect_subexpressions(result, seen)
        self.right._collect_subexpressions(result, seen)
        expression = self.to_expression()
        if expression not in seen:
            seen.add(expression)
            result.append(expression)


@dataclass(frozen=True)
class EqNode(AstNode):
    left: AstNode
    right: AstNode

    def evaluate(self, values: dict[str, int]) -> int:
        return 1 if self.left.evaluate(values) == self.right.evaluate(values) else 0

    def collect_variables(self) -> set[str]:
        return self.left.collect_variables() | self.right.collect_variables()

    def to_expression(self) -> str:
        return f"({self.left.to_expression()}~{self.right.to_expression()})"

    def fill_expression_values(self, values: dict[str, int], target: dict[str, int]) -> int:
        left_value = self.left.fill_expression_values(values, target)
        right_value = self.right.fill_expression_values(values, target)
        result = 1 if left_value == right_value else 0
        target[self.to_expression()] = result
        return result

    def _collect_subexpressions(self, result: list[str], seen: set[str]) -> None:
        self.left._collect_subexpressions(result, seen)
        self.right._collect_subexpressions(result, seen)
        expression = self.to_expression()
        if expression not in seen:
            seen.add(expression)
            result.append(expression)