# Documentación del Lexer

Dentro de la estructura dle proyecto, tenemos la carpeta Lexer, que inclute dos archivos importantes, el lexer.py y el tokens.py

El LEXER es el punto actual en que nos encontramos a la hora de redactar este documento

```bash
tafak/
│
├── codigos/                 # Programas TAFAK para pruebas manuales
│     ├── hola.taf
│     ├── funciones.taf
│     └── ...
│
├── src/                     
│   │
│   ├── lexer/               # *Módulo de análisis léxico*
│   │     ├── __init__.py
│   │     ├── tokens.py      # Definición de Token, TokenType, KEYWORDS, TYPES, BOOLS
│   │     └── lexer.py       # Lexer completo: convierte texto → tokens
│   │
│   ├── parser/              # (Próxima etapa) Análisis sintáctico → AST
│   │     ├── __init__.py
│   │     ├── parser.py      # Parser principal
│   │     └── nodes.py       # Definiciones de nodos del AST
│   │
│   ├── sema/                # (Futuro) Análisis semántico
│   │     ├── __init__.py
│   │     └── typechecker.py # Verificación de tipos
│   │
│   ├── codegen/             # (Futuro) Generación de código Python
│         ├── __init__.py
│         └── python_codegen.py
│
├── test/                    # Pruebas oficiales del lenguaje
│     ├── __init__.py
│     └── test_lexer.py      # Archivo para probar el lexer usando códigos de /codigos
│
├── docs/                    # Documentación del proyecto
│     ├── lexer.md
│     ├── parser.md
│     └── spec.md
│
├── README.md                # Documento principal del proyecto
└── pyproject.toml / setup.py (opcional)  # Configuración del paquete
```

# TAFAK — Módulo de Análisis Léxico (lexer/)

El análisis léxico es la primera etapa del compilador/intérprete de TAFAK.
Su función es transformar el código fuente (.taf) en una secuencia de tokens, que representan unidades significativas del lenguaje.

- Este documento explica:
- cómo funcionan los tokens
- cómo opera el lexer
- cómo leer la salida de tokenización
- cómo se diseñaron las pruebas

## 1. ¿Qué es un token?

Un token es una estructura que representa un elemento del lenguaje:

palabras clave (ej: ti, macorróca, wá)
identificadores (ej: x, edad, doble)
números
strings
operadores
símbolos del lenguaje ((, {, ;…)

En TAFAK todos los tokens incluyen:

type — categoría (KEYWORD, TYPE, IDENT, NUMBER, etc.)

value — contenido textual

line — línea donde aparece

column — columna donde aparece

## 2. Estructura del módulo léxico
```bash
src/
 └── lexer/
       ├── tokens.py
       ├── lexer.py
       └── __init__.py
```

## 3. Archivo tokens.py

Este archivo define:

✔ TokenType

Una enumeración con todos los tipos válidos de token.
```python
class TokenType(Enum):
    KEYWORD = auto()
    TYPE = auto()
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()
    CHAR = auto()
    BOOL = auto()
    OPERATOR = auto()
    SYMBOL = auto()
    EOF = auto()
```
✔ Token

Objeto que el lexer devuelve.
```python
class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
```
✔ Tablas de palabras reservadas

TAFAK define tres grupos de lexemas especiales:

1) KEYWORDS

Control de flujo, funciones, E/S, etc.
```
KEYWORDS = {
    "ti",
    "macorróca",
    "lúri",
    "wá",
    "pa",
    "Iherré",
    ...
}
```
2) TYPES
```
TYPES = {
    "chátené",
    "terminá",
    "allima",
    ...
}
```
3) BOOLS
```
BOOLS = {
    "tócu": True,
    "maíca": False
}
```
## 4. Archivo lexer.py

El lexer recorre el código fuente carácter por carácter y construye tokens.

### 4.1. Constructor
```python
def __init__(self, source: str):
    self.source = source
    self.pos = 0
    self.line = 1
    self.column = 1
```

Mantiene:

pos: índice actual en source

line y column: posición para mensajes de error

### 4.2. Funciones básicas

**peek()**

Devuelve el carácter actual sin avanzar.

**advance()**

Avanza un carácter, actualizando columna y línea.

**match_regex(pattern)**

Evalúa un patrón regex desde la posición actual.

**make_token(type, value, line, column)**

Crea un objeto Token listo para devolver.

### 4.3. skip_whitespace_and_comments()

Ignora:

espacios, tabs, saltos de línea, comentarios tipo //
Esto garantiza que los tokens solo representen contenido significativo.

### 4.4. next_token()

La función más importante del módulo.
Devuelve un solo token cada vez que se llama.

Su orden de análisis es:

```bash
EOF

símbolos simples → (, ), {, }, ;, ,

operadores de dos caracteres → ==, >=, <=, ><

operadores de un carácter → +, -, *, %, <, >…

números

strings ("texto")

caracteres ('a')

identificadores → keywords, types, bools o nombres de variables

Cada token incluye:

tipo

valor

línea

columna
```

Si encuentra un carácter no reconocido → lanza error.

### 4.5. tokenize()

Convierte todo el archivo .taf en una lista de tokens.

```python
def tokenize(self):
    tokens = []
    tok = self.next_token()

    while tok.type != TokenType.EOF:
        tokens.append(tok)
        tok = self.next_token()

    tokens.append(tok)   # EOF
    return tokens
```

## 5. Uso del lexer

Ejemplo básico:
```python
from src.lexer.lexer import Lexer

codigo = 'ti chátené x = 5;'
lexer = Lexer(codigo)
tokens = lexer.tokenize()

for t in tokens:
    print(t)
```

Salida:
```bash
Token(KEYWORD, 'ti')
Token(TYPE, 'chátené')
Token(IDENT, 'x')
Token(OPERATOR, '=')
Token(NUMBER, 5)
Token(SYMBOL, ';')
Token(EOF, 'EOF')
```

## 6. Carpeta codigos/ para pruebas manuales

Ejemplo: codigos/funciones.taf
```
macorróca chátené doble(chátené x) {
    lúri x * 2;
}

macorróca chátené main() {
    Iherré(doble(4));
    lúri 0;
}
```
## 7. Test oficial (test/test_lexer.py)
```python
from src.lexer.lexer import Lexer

archivo = "codigos/funciones.taf"

with open(archivo, "r", encoding="utf8") as f:
    codigo = f.read()

print(f"\n=== Analizando: {archivo} ===\n")

lexer = Lexer(codigo)
tokens = lexer.tokenize()

for t in tokens:
    print(t)
```

Ejecutar desde la raíz del proyecto:

python -m test.test_lexer

## 8. Ejemplo de salida real de tokenización
```bash
Token(KEYWORD, 'macorróca', 1:1)
Token(TYPE, 'chátené', 1:11)
Token(IDENT, 'doble', 1:19)
Token(SYMBOL, '(', 1:24)
Token(TYPE, 'chátené', 1:25)
Token(IDENT, 'x', 1:33)
Token(SYMBOL, ')', 1:34)
Token(SYMBOL, '{', 1:36)
Token(KEYWORD, 'lúri', 2:5)
Token(IDENT, 'x', 2:10)
Token(OPERATOR, '*', 2:12)
Token(NUMBER, 2, 2:14)
Token(SYMBOL, ';', 2:15)
Token(SYMBOL, '}', 3:1)
Token(KEYWORD, 'macorróca', 5:1)
Token(TYPE, 'chátené', 5:11)
Token(KEYWORD, 'main', 5:19)
Token(SYMBOL, '(', 5:23)
Token(SYMBOL, ')', 5:24)
Token(SYMBOL, '{', 5:26)
Token(KEYWORD, 'Iherré', 6:5)
Token(SYMBOL, '(', 6:11)
Token(IDENT, 'doble', 6:12)
Token(SYMBOL, '(', 6:17)
Token(NUMBER, 4, 6:18)
Token(SYMBOL, ')', 6:19)
Token(SYMBOL', ')', 6:20)
Token(SYMBOL', ';', 6:21)
Token(KEYWORD, 'lúri', 7:5)
Token(NUMBER, 0, 7:10)
Token(SYMBOL, ';', 7:11)
Token(SYMBOL, '}', 8:1)
Token(EOF, 'EOF', 9:1)
```

Esto demuestra que el lexer reconoce correctamente:

funciones

parámetros

return

bloques

llamadas anidadas

operadores

números

strings

EOF

## 9. Estado actual del módulo

✔ Lexer estable
✔ Manejo correcto de Unicode
✔ Soporte para funciones, tipos, operadores, literales, booleanos
✔ Lista de tokens consistente para el parser