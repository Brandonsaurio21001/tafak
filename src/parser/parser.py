# parser.py
# Parser recursivo de TAFAK (v1)
from src.lexer.tokens import TokenType
from src.parser.nodes import (
    Program, FunctionDecl, VarDecl, Block, IfStmt, WhileStmt,
    ReturnStmt, ExprStmt,
    BinaryOp, UnaryOp, Literal, Variable, CallExpr
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # -------------------------
    # utilidades
    # -------------------------

    def peek(self):
        return self.tokens[self.pos]

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def match(self, *types):
        """Avanza si el tipo coincide."""
        if self.peek().type in types:
            return self.advance()
        return None

    def expect(self, type_, msg):
        """Consume un token o lanza error"""
        tok = self.peek()
        if tok.type != type_:
            raise Exception(f"{msg} en línea {tok.line}:{tok.column}")
        return self.advance()

    # -------------------------
    # inicio del parser
    # -------------------------

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        declarations = []

        while self.peek().type != TokenType.EOF:
            declarations.append(self.parse_declaration())

        return Program(declarations)

    # -------------------------
    # declaraciones (funciones, vars)
    # -------------------------

    def parse_declaration(self):
        tok = self.peek()
        
        if tok.type == TokenType.KEYWORD and tok.value == "macorróca":
            return self.parse_function()
        
        if tok.type == TokenType.KEYWORD and tok.value == "ti":
            return self.parse_var_decl()
        
        return self.parse_statement()

    # -------------------------
    # statements
    # -------------------------

    def parse_statement(self):
        # será implementado después
        raise NotImplementedError

    # -------------------------
    # expresiones (vendrá pronto)
    # -------------------------

    def parse_expression(self):
        raise NotImplementedError
