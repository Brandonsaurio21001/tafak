# nodes.py
# Nodos del AST para TAFAK v1

class Program:
    def __init__(self, declarations):
        self.declarations = declarations    # lista de nodos (funciones, vars)

    def __repr__(self):
        return f"Program({self.declarations!r})"


# -----------------------
# Declaraciones top-level
# -----------------------

class FunctionDecl:
    def __init__(self, name, params, return_type, body):
        self.name = name              # string
        self.params = params          # lista de (tipo, nombre)
        self.return_type = return_type
        self.body = body              # Block

    def __repr__(self):
        return f"FunctionDecl({self.name}, params={self.params}, return={self.return_type})"


class VarDecl:
    def __init__(self, name, var_type, initializer):
        self.name = name
        self.var_type = var_type
        self.initializer = initializer   # expr o None

    def __repr__(self):
        return f"VarDecl({self.name}:{self.var_type} = {self.initializer})"


# -----------------------
# Sentencias
# -----------------------

class Block:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"


class IfStmt:
    def __init__(self, condition, then_block, else_block):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def __repr__(self):
        return f"If({self.condition}, then={self.then_block}, else={self.else_block})"


class WhileStmt:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"While({self.condition}, {self.body})"


class ReturnStmt:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"


class ExprStmt:
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"ExprStmt({self.expr})"


# -----------------------
# Expresiones
# -----------------------

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"


class UnaryOp:
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.op}{self.right})"


class Literal:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value!r}"


class Variable:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"


class CallExpr:
    def __init__(self, callee, args):
        self.callee = callee
        self.args = args

    def __repr__(self):
        return f"Call({self.callee}, args={self.args})"
