# Traductor Python a JavaScript ES6

Un compilador completo que traduce código Python 3 a JavaScript ES6, implementando todas las fases del pipeline de compilación.

## Características

### Pipeline Completo de Compilación
- **Análisis Léxico**: Tokenización del código fuente Python
- **Análisis Sintáctico**: Construcción del Árbol de Sintaxis Abstracta (AST)
- **Análisis Semántico**: Validación de tipos y tabla de símbolos
- **Generación de Código**: Traducción a JavaScript ES6

### Funcionalidades Soportadas
- Funciones y parámetros
- Estructuras de control (if/else, for, while)
- Operadores aritméticos y lógicos
- Listas y diccionarios
- Clases básicas
- Recursión
- Variables y asignaciones
- Llamadas a funciones

## Estructura del Proyecto

```
ProyectoFinalCompiladores/
├── lexer.py              # Analizador léxico
├── ast_nodes.py          # Definición de nodos del AST
├── parser.py             # Analizador sintáctico
├── semantic_analyzer.py  # Analizador semántico
├── code_generator.py     # Generador de código JavaScript
├── compiler.py           # Compilador principal
├── gui.py               # Interfaz gráfica
├── main.py              # Script principal
├── test_examples.py     # Ejemplos de prueba
└── README.md            # Documentación
```

## Instalación y Uso

### Requisitos
- Python 3.7+
- tkinter (incluido en la mayoría de instalaciones de Python)

### Ejecución

#### Interfaz Gráfica (Recomendado)
```bash
python main.py
```

#### Modo Interactivo
```bash
python main.py -i
```

#### Compilar Archivo
```bash
python main.py -c archivo.py
python main.py -c archivo.py -o salida.js
```

#### Ejecutar Pruebas
```bash
python test_examples.py
```

## Ejemplos de Uso

### Ejemplo 1: Función Simple
**Python:**
```python
def saludar(nombre):
    return "Hola, " + nombre

mensaje = saludar("Mundo")
print(mensaje)
```

**JavaScript Generado:**
```javascript
function saludar(nombre) {
  return ("Hola, " + nombre);
}

let mensaje = saludar("Mundo");
console.log(mensaje);
```

### Ejemplo 2: Estructuras de Control
**Python:**
```python
def clasificar(n):
    if n > 0:
        return "positivo"
    else:
        return "negativo"

for i in range(3):
    resultado = clasificar(i)
    print(resultado)
```

**JavaScript Generado:**
```javascript
function clasificar(n) {
  if ((n > 0)) {
    return "positivo";
  } else {
    return "negativo";
  }
}

for (const i of Array.from({length: 3}, (_, i) => i)) {
  let resultado = clasificar(i);
  console.log(resultado);
}
```

## Arquitectura del Compilador

### 1. Analizador Léxico (lexer.py)
- Convierte el código fuente en tokens
- Maneja indentación de Python
- Reconoce palabras clave, operadores y literales

### 2. Analizador Sintáctico (parser.py)
- Implementa gramática recursiva descendente
- Construye el AST siguiendo la precedencia de operadores
- Maneja estructuras de control y definiciones

### 3. Analizador Semántico (semantic_analyzer.py)
- Tabla de símbolos con manejo de scopes
- Validación de declaraciones y uso de variables
- Verificación de tipos básicos

### 4. Generador de Código (code_generator.py)
- Traduce nodos del AST a JavaScript ES6
- Mapea funciones built-in de Python
- Genera código con indentación apropiada

## Limitaciones Actuales

- No soporta herencia de clases
- Manejo básico de tipos
- No incluye todas las funciones built-in de Python
- No maneja excepciones
- No soporta imports/modules

## Extensiones Futuras

- Soporte completo para POO
- Manejo de excepciones
- Sistema de módulos
- Optimizaciones de código
- Mejor inferencia de tipos
- Soporte para async/await

## Contribución

Este proyecto fue desarrollado como parte del curso de Compiladores. Las contribuciones son bienvenidas para extender las funcionalidades.

## Licencia

Proyecto académico - Universidad [Nombre]
