# tokens.py
# Definición de tokens para TAFAK v1

from enum import Enum, auto


class TokenType(Enum):
    # Palabras clave
    KEYWORD = auto()
    TYPE = auto()
    BOOL = auto()

    # Identificadores
    IDENT = auto()

    # Literales
    NUMBER = auto()
    STRING = auto()
    CHAR = auto()

    # Operadores
    OPERATOR = auto()

    # Símbolos: (, ), {, }, ;, ,
    SYMBOL = auto()

    # Fin del archivo
    EOF = auto()


class Token:
    """
    Representa un token individual del lenguaje TAFAK.
    Contiene:
    - type  -> tipo de token (TokenType)
    - value -> valor (string, número, etc.)
    - line  -> línea en el código fuente
    - column -> columna en el código fuente
    """

    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.column})"


# -------------------------------------------------------------------
# TABLAS DE PALABRAS CLAVE – definidas desde la especificación TAFAK
# -------------------------------------------------------------------

KEYWORDS = {
    "ti",
    "const",
    "macorróca",
    "masálaca",
    "wá",
    "pa",
    "ótacá",
    "Ihoné",
    "lúri",
    "cuá",
    "Iherré",
    "main"
}

TYPES = {
    "chátené",
    "lhajáia",
    "aquí",
    "usírra",
    "malhióca"
}

BOOLS = {
    "tócu": True,
    "maíca": False
}
