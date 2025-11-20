from lexer import Lexer

code = """def saludar(nombre):
    return "Hola, " + nombre

resultado = saludar("Mundo")
print(resultado)"""

print("Código:")
print(repr(code))
print("\nTokens:")

lexer = Lexer(code)
tokens = lexer.tokenize()

for i, token in enumerate(tokens):
    print(f"{i:2d}: {token.type.name:12} {repr(token.value):15} (line {token.line}, col {token.column})")
