# lexer.py
# Lexer oficial de TAFAK v1

import re
#from tokens import Token, TokenType, KEYWORDS, TYPES, BOOLS
#from src.lexer.tokens import Token, TokenType, KEYWORDS, TYPES, BOOLS
from .tokens import Token, TokenType, KEYWORDS, TYPES, BOOLS


class Lexer:
    def __init__(self, source: str):
        self.source = source       # código fuente en string
        self.pos = 0               # índice actual
        self.line = 1              # línea actual
        self.column = 1            # columna actual

    # ---------------------------------------------------------
    # Mirar el carácter actual sin avanzar
    # ---------------------------------------------------------
    def peek(self):
        if self.pos >= len(self.source):
            return '\0'  # Fin del texto
        return self.source[self.pos]

    # ---------------------------------------------------------
    # Avanza un carácter y retorna ese carácter
    # ---------------------------------------------------------
    def advance(self):
        ch = self.peek()
        self.pos += 1

        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return ch

    # ---------------------------------------------------------
    # Coincide un patrón regex desde la posición actual
    # ---------------------------------------------------------
    def match_regex(self, pattern):
        regex = re.compile(pattern)
        match = regex.match(self.source, self.pos)
        return match

    # ---------------------------------------------------------
    # Crear token
    # ---------------------------------------------------------
    def make_token(self, type, value, line=None, column=None):
        return Token(type, value, line or self.line, column or self.column)

    # ---------------------------------------------------------
    # Ignorar espacios y comentarios
    # ---------------------------------------------------------
    def skip_whitespace_and_comments(self):
        while True:
            ch = self.peek()

            # Espacios
            if ch in " \t\r\n":
                self.advance()
                continue

            # Comentarios tipo //
            if self.source.startswith("//", self.pos):
                while self.peek() not in ['\n', '\0']:
                    self.advance()
                continue

            break  # no más cosas que ignorar

    # ---------------------------------------------------------
    # Token principal
    # ---------------------------------------------------------
    def next_token(self):
        self.skip_whitespace_and_comments()

        start_line = self.line
        start_column = self.column
        ch = self.peek()

        # 1) Fin del archivo
        if ch == '\0':
            return self.make_token(TokenType.EOF, "EOF", start_line, start_column)

        # 2) Símbolos sueltos
        if ch in "(){};,":  
            self.advance()
            return self.make_token(TokenType.SYMBOL, ch, start_line, start_column)

        # 3) Operadores multi-caracter
        if self.source.startswith("==", self.pos):
            self.pos += 2
            self.column += 2
            return self.make_token(TokenType.OPERATOR, "==", start_line, start_column)

        if self.source.startswith("><", self.pos):
            self.pos += 2
            self.column += 2
            return self.make_token(TokenType.OPERATOR, "><", start_line, start_column)

        if self.source.startswith("<=", self.pos):
            self.pos += 2
            self.column += 2
            return self.make_token(TokenType.OPERATOR, "<=", start_line, start_column)

        if self.source.startswith(">=", self.pos):
            self.pos += 2
            self.column += 2
            return self.make_token(TokenType.OPERATOR, ">=", start_line, start_column)

        # 4) Operadores de un carácter
        if ch in "+-*/%<>=!":
            self.advance()
            return self.make_token(TokenType.OPERATOR, ch, start_line, start_column)

        # 5) Números
        number_regex = r"[0-9]+(\.[0-9]+)?"
        match = self.match_regex(number_regex)
        if match:
            lexeme = match.group(0)
            self.pos += len(lexeme)
            self.column += len(lexeme)

            if "." in lexeme:
                return self.make_token(TokenType.NUMBER, float(lexeme), start_line, start_column)
            else:
                return self.make_token(TokenType.NUMBER, int(lexeme), start_line, start_column)

        # 6) Strings
        if ch == '"':
            self.advance()  # consumir "
            value = ""
            while True:
                c = self.advance()
                if c == '"':
                    break
                if c == '\0':
                    raise Exception("String sin cerrar")
                value += c
            return self.make_token(TokenType.STRING, value, start_line, start_column)

        # 7) Caracter
        if ch == "'":
            self.advance()
            c = self.advance()
            if self.advance() != "'":
                raise Exception("Carácter mal formado")
            return self.make_token(TokenType.CHAR, c, start_line, start_column)

        # 8) Identificadores (unicode-friendly)
        ident_regex = r"[\wáéíóúÁÉÍÓÚüÜñÑ]+"
        match = self.match_regex(ident_regex)
        if match:
            lex = match.group(0)
            self.pos += len(lex)
            self.column += len(lex)

            if lex in KEYWORDS:
                return self.make_token(TokenType.KEYWORD, lex, start_line, start_column)

            if lex in TYPES:
                return self.make_token(TokenType.TYPE, lex, start_line, start_column)

            if lex in BOOLS:
                return self.make_token(TokenType.BOOL, BOOLS[lex], start_line, start_column)

            return self.make_token(TokenType.IDENT, lex, start_line, start_column)

        # Error
        raise Exception(f"Caracter inesperado '{ch}' en {self.line}:{self.column}")

    # ---------------------------------------------------------
    # Tokenizar todo el archivo
    # ---------------------------------------------------------
    def tokenize(self):
        tokens = []
        tok = self.next_token()
        while tok.type != TokenType.EOF:
            tokens.append(tok)
            tok = self.next_token()
        tokens.append(tok)
        return tokens
