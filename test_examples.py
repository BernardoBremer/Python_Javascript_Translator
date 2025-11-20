#!/usr/bin/env python3
"""
Ejemplos de prueba para el traductor Python → JavaScript
"""

# Ejemplo 1: Funciones básicas
def ejemplo_funciones():
    return '''
def saludar(nombre):
    return "Hola, " + nombre

def sumar(a, b):
    return a + b

resultado = sumar(5, 3)
mensaje = saludar("Mundo")
print(mensaje)
print(resultado)
'''

# Ejemplo 2: Estructuras de control
def ejemplo_control():
    return '''
def clasificar_numero(n):
    if n > 0:
        return "positivo"
    elif n < 0:
        return "negativo"
    else:
        return "cero"

for i in range(-2, 3):
    tipo = clasificar_numero(i)
    print("El número", i, "es", tipo)
'''

# Ejemplo 3: Listas y bucles
def ejemplo_listas():
    return '''
def procesar_lista(numeros):
    resultado = []
    for num in numeros:
        if num % 2 == 0:
            print("Par:", num * 2)
        else:
            print("Impar:", num * 3)
    return resultado

lista_original = [1, 2, 3, 4, 5]
procesar_lista(lista_original)
'''

# Ejemplo 4: Recursión
def ejemplo_recursion():
    return '''
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(1, 6):
    fact = factorial(i)
    fib = fibonacci(i)
    print("factorial(", i, ") =", fact, ", fibonacci(", i, ") =", fib)
'''

# Ejemplo 5: Operaciones matemáticas
def ejemplo_matematicas():
    return '''
def operaciones_basicas(x, y):
    suma = x + y
    resta = x - y
    multiplicacion = x * y
    division = x / y
    modulo = x % y
    potencia = x ** y
    
    print(x, "+", y, "=", suma)
    print(x, "-", y, "=", resta)
    print(x, "*", y, "=", multiplicacion)
    print(x, "/", y, "=", division)
    print(x, "%", y, "=", modulo)
    print(x, "**", y, "=", potencia)

operaciones_basicas(10, 3)
'''

# Ejemplo 6: Clases básicas
def ejemplo_clases():
    return '''
class Persona:
    def saludar(self):
        return "Hola, soy una persona"

persona = Persona()
mensaje = persona.saludar()
print(mensaje)
'''

def ejecutar_pruebas():
    """Ejecuta todas las pruebas de ejemplo"""
    from compiler import PythonToJSCompiler, CompilerError
    
    ejemplos = [
        ("Funciones básicas", ejemplo_funciones()),
        ("Estructuras de control", ejemplo_control()),
        ("Listas y bucles", ejemplo_listas()),
        ("Recursión", ejemplo_recursion()),
        ("Operaciones matemáticas", ejemplo_matematicas()),
        ("Clases básicas", ejemplo_clases())
    ]
    
    compiler = PythonToJSCompiler()
    
    print("=== EJECUTANDO PRUEBAS DEL TRADUCTOR ===\n")
    
    for i, (nombre, codigo) in enumerate(ejemplos, 1):
        print(f"Prueba {i}: {nombre}")
        print("-" * 50)
        
        try:
            js_code = compiler.compile(codigo)
            print("✓ COMPILACIÓN EXITOSA")
            print("\nCódigo JavaScript generado:")
            print(js_code)
            
        except CompilerError as e:
            print(f"✗ ERROR DE COMPILACIÓN: {e}")
        
        except Exception as e:
            print(f"✗ ERROR INESPERADO: {e}")
        
        print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    ejecutar_pruebas()
