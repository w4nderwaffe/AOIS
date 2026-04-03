from ast_nodes import AndNode, AstNode, EqNode, ImplNode, NotNode, OrNode, VariableNode
from errors import ParserError
from tokens import (
    TOKEN_AND,
    TOKEN_EOF,
    TOKEN_EQ,
    TOKEN_IMPL,
    TOKEN_LPAREN,
    TOKEN_NOT,
    TOKEN_OR,
    TOKEN_RPAREN,
    TOKEN_VAR,
    Token,
)


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.position = 0

    def parse(self) -> AstNode:
        if len(self.tokens) == 0:
            raise ParserError("Список токенов пуст")
        node = self._parse_equivalence()
        if self._current().kind != TOKEN_EOF:
            token = self._current()
            raise ParserError(f"Лишний токен '{token.value}' в позиции {token.position}")
        return node

    def _parse_equivalence(self) -> AstNode:
        node = self._parse_implication()
        while self._current().kind == TOKEN_EQ:
            self._consume(TOKEN_EQ)
            right = self._parse_implication()
            node = EqNode(node, right)
        return node

    def _parse_implication(self) -> AstNode:
        node = self._parse_or()
        if self._current().kind == TOKEN_IMPL:
            self._consume(TOKEN_IMPL)
            right = self._parse_implication()
            return ImplNode(node, right)
        return node

    def _parse_or(self) -> AstNode:
        node = self._parse_and()
        while self._current().kind == TOKEN_OR:
            self._consume(TOKEN_OR)
            right = self._parse_and()
            node = OrNode(node, right)
        return node

    def _parse_and(self) -> AstNode:
        node = self._parse_not()
        while self._current().kind == TOKEN_AND:
            self._consume(TOKEN_AND)
            right = self._parse_not()
            node = AndNode(node, right)
        return node

    def _parse_not(self) -> AstNode:
        if self._current().kind == TOKEN_NOT:
            self._consume(TOKEN_NOT)
            return NotNode(self._parse_not())
        return self._parse_primary()

    def _parse_primary(self) -> AstNode:
        current = self._current()

        if current.kind == TOKEN_VAR:
            token = self._consume(TOKEN_VAR)
            return VariableNode(token.value)

        if current.kind == TOKEN_LPAREN:
            self._consume(TOKEN_LPAREN)
            node = self._parse_equivalence()
            self._consume(TOKEN_RPAREN)
            return node

        if current.kind == TOKEN_EOF:
            raise ParserError("Неожиданный конец выражения")

        raise ParserError(f"Неожиданный токен '{current.value}' в позиции {current.position}")

    def _current(self) -> Token:
        return self.tokens[self.position]

    def _consume(self, kind: str) -> Token:
        current = self._current()
        if current.kind != kind:
            raise ParserError(
                f"Ожидался токен типа '{kind}', получен '{current.kind}' в позиции {current.position}"
            )
        self.position += 1
        return current