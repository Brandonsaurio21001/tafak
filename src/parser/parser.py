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


    def parse_function(self):
        """Vamos a construir el nodo de fucnión que definimos en nodes.py
        FunctionDecl
        ├── name: "doble"
        ├── return_type: "chátené"
        ├── params:
        │     └── ("chátené", "x")
        └── body: Block
                └── statements:
                        └── ReturnStmt
                                └── BinaryOp
                                    ├── left: Variable("x")
                                    ├── op: "*"
                                    └── right: Literal(2)

        """
        #consumir macorroca
        self.expect(TokenType.KEYWORD, "se esperaba 'macorróca'")
        #construir el tipo de retonro
        ret_type = self.expect(TokenType.TYPE, "Se esperaba tipo de retorno").value
        #constuir el nombre de la funcion
        name = self.expect(TokenType.IDENT)
        #los argumentos
        self.expect(TokenType.SYMBOL, "se esperaba '('")
        params = self.parse_parameters()
        self.expect(TokenType.SYMBOL, "se esperaba ')'")
        #armar el cuerpo
        body = self.parse_block()

        return FunctionDecl(name, params, ret_type, body)


    def parse_parameters(self):
        params = []
        # caso de que no lleve parametros, como el main()
        if self.peek().value == ")":
            return params
        
        while True:
            #tipo
            t = self.expect(TokenType.TYPE, "se esperaba tipo de parámetro").value
            #nombre
            n = self.expect(TokenType.IDENT, "se esperaba un nombre de parámetro").value

            params.append((t,n))

            #si hay una coma, seguimos
            if self.peek().value == ",":
                self.advance()
                continue

            break
        return params
    
    def parse_block(self):
        self.expect(TokenType.SYMBOL, "se esperaba '{'")
        statements = []
        #vamonos hasta }
        while not (self.peek().type == TokenType.SYMBOL and self.peek().value == "}"):
            statements.append(self.parse_statement())
        
        self.expect(TokenType.SYMBOL, "se esperaba un '}'")
        return Block(statements)
    
    def parse_var_decl(self):
        #consumir ti
        self.expect(TokenType.KEYWORD, "se esperaba 'ti'")
        #ver el tipo
        var_type = self.expect(TokenType.TYPE, "se esperaba tipo de variable").value
        #nombre
        name = self.expect(TokenType.IDENT, "se esperaba nombre de variable").value

        initializer = None
        if self.peek().value == "=":
            self.advance()
            initializer = self.parse_expression()

        self.expect(TokenType.SYMBOL, "se esperaba ';'")

        return VarDecl(name, var_type, initializer)











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



