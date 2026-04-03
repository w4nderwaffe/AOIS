import pytest

from errors import LexerError
from lexer import Lexer
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
)


def token_kinds(text: str) -> list[str]:
    return [token.kind for token in Lexer(text).tokenize()]


def test_lexer_simple_expression():
    kinds = token_kinds("(!a&b)|c")
    assert kinds == [
        TOKEN_LPAREN,
        TOKEN_NOT,
        TOKEN_VAR,
        TOKEN_AND,
        TOKEN_VAR,
        TOKEN_RPAREN,
        TOKEN_OR,
        TOKEN_VAR,
        TOKEN_EOF,
    ]


def test_lexer_supports_unicode_symbols():
    kinds = token_kinds("¬a∧b∨c→d")
    assert kinds == [
        TOKEN_NOT,
        TOKEN_VAR,
        TOKEN_AND,
        TOKEN_VAR,
        TOKEN_OR,
        TOKEN_VAR,
        TOKEN_IMPL,
        TOKEN_VAR,
        TOKEN_EOF,
    ]


def test_lexer_supports_equivalence():
    kinds = token_kinds("a~b")
    assert kinds == [TOKEN_VAR, TOKEN_EQ, TOKEN_VAR, TOKEN_EOF]


def test_lexer_skips_spaces():
    kinds = token_kinds("  a   ->   b  ")
    assert kinds == [TOKEN_VAR, TOKEN_IMPL, TOKEN_VAR, TOKEN_EOF]


def test_lexer_invalid_symbol():
    with pytest.raises(LexerError):
        Lexer("a+x").tokenize()


def test_lexer_invalid_variable():
    with pytest.raises(LexerError):
        Lexer("x").tokenize()


def test_lexer_invalid_implication():
    with pytest.raises(LexerError):
        Lexer("a-b").tokenize()


def test_lexer_read_variable_direct_error():
    lexer = Lexer("!")
    with pytest.raises(LexerError):
        lexer._read_variable()