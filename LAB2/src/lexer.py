from errors import LexerError
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


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.position = 0

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []

        while True:
            self._skip_spaces()
            current = self._current_char()

            if current is None:
                tokens.append(Token(TOKEN_EOF, "", self.position))
                return tokens

            if current in "abcde":
                tokens.append(self._read_variable())
                continue

            if current in ("!", "¬"):
                tokens.append(Token(TOKEN_NOT, current, self.position))
                self.position += 1
                continue

            if current in ("&", "∧"):
                tokens.append(Token(TOKEN_AND, current, self.position))
                self.position += 1
                continue

            if current in ("|", "∨"):
                tokens.append(Token(TOKEN_OR, current, self.position))
                self.position += 1
                continue

            if current == "~":
                tokens.append(Token(TOKEN_EQ, current, self.position))
                self.position += 1
                continue

            if current == "(":
                tokens.append(Token(TOKEN_LPAREN, current, self.position))
                self.position += 1
                continue

            if current == ")":
                tokens.append(Token(TOKEN_RPAREN, current, self.position))
                self.position += 1
                continue

            if current == "-":
                tokens.append(self._read_impl())
                continue

            if current == "→":
                tokens.append(Token(TOKEN_IMPL, current, self.position))
                self.position += 1
                continue

            raise LexerError(f"Недопустимый символ '{current}' в позиции {self.position}")

    def _skip_spaces(self) -> None:
        while self.position < len(self.text) and self.text[self.position].isspace():
            self.position += 1

    def _read_variable(self) -> Token:
        current = self._current_char()
        if current is None or current not in "abcde":
            raise LexerError(f"Ожидалась переменная в позиции {self.position}")
        token = Token(TOKEN_VAR, current, self.position)
        self.position += 1
        return token

    def _read_impl(self) -> Token:
        start = self.position
        if self.position + 1 < len(self.text) and self.text[self.position:self.position + 2] == "->":
            self.position += 2
            return Token(TOKEN_IMPL, "->", start)
        raise LexerError(f"Ожидалась операция '->' в позиции {self.position}")

    def _current_char(self) -> str | None:
        if self.position >= len(self.text):
            return None
        return self.text[self.position]