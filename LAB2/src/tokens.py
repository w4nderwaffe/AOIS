from dataclasses import dataclass

TOKEN_VAR = "VAR"
TOKEN_NOT = "NOT"
TOKEN_AND = "AND"
TOKEN_OR = "OR"
TOKEN_IMPL = "IMPL"
TOKEN_EQ = "EQ"
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_EOF = "EOF"


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int