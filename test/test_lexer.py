from src.lexer.lexer import Lexer


archivo = "codigos/funciones.taf"

with open(archivo, "r", encoding="utf8") as f:
    codigo = f.read()

print(f"\n=== Analizando: {archivo} ===\n")

lexer = Lexer(codigo)
tokens = lexer.tokenize()

for t in tokens:
    print(t)
