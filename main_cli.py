#!/usr/bin/env python3
"""
Traductor Python a JavaScript ES6
Proyecto Final - Compiladores

Uso:
    python main.py                    # Interfaz gráfica
    python main.py -c file.py         # Compilar archivo
    python main.py -i                 # Modo interactivo
"""

import sys
import argparse
from compiler import PythonToJSCompiler, CompilerError

def interactive_mode():
    """Modo interactivo de línea de comandos"""
    compiler = PythonToJSCompiler()
    
    print("=== Traductor Python → JavaScript ES6 ===")
    print("Modo interactivo. Escriba 'exit' para salir.")
    print("Escriba 'help' para ver comandos disponibles.\n")
    
    while True:
        try:
            command = input(">>> ").strip()
            
            if command.lower() in ['exit', 'quit']:
                print("¡Hasta luego!")
                break
            
            elif command.lower() == 'help':
                print_help()
                continue
            
            elif command.lower() == 'clear':
                import os
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            elif command.lower().startswith('file '):
                filename = command[5:].strip()
                compile_file_interactive(compiler, filename)
                continue
            
            elif command.lower() == 'example':
                show_example(compiler)
                continue
            
            elif not command:
                continue
            
            # Compilar código directo
            print("\nIngrese su código Python (termine con una línea vacía):")
            lines = []
            while True:
                line = input()
                if not line:
                    break
                lines.append(line)
            
            if lines:
                python_code = '\n'.join(lines)
                compile_code_interactive(compiler, python_code)
        
        except KeyboardInterrupt:
            print("\n¡Hasta luego!")
            break
        except EOFError:
            print("\n¡Hasta luego!")
            break

def compile_file_interactive(compiler, filename):
    """Compila un archivo en modo interactivo"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            python_code = f.read()
        
        print(f"\nCompilando archivo: {filename}")
        js_code = compiler.compile(python_code)
        
        output_file = filename.replace('.py', '.js')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_code)
        
        print(f"✓ Compilación exitosa: {output_file}")
        
    except FileNotFoundError:
        print(f"✗ Error: Archivo '{filename}' no encontrado")
    except CompilerError as e:
        print(f"✗ Error de compilación: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

def compile_code_interactive(compiler, python_code):
    """Compila código en modo interactivo"""
    try:
        js_code = compiler.compile(python_code)
        print("\n" + "="*50)
        print("CÓDIGO JAVASCRIPT GENERADO:")
        print("="*50)
        print(js_code)
        print("="*50)
        
    except CompilerError as e:
        print(f"✗ Error de compilación: {e}")

def show_example(compiler):
    """Muestra un ejemplo de compilación"""
    example_code = '''def saludar(nombre):
    mensaje = "Hola, " + nombre + "!"
    print(mensaje)
    return mensaje

def main():
    nombres = ["Ana", "Carlos", "María"]
    for nombre in nombres:
        saludar(nombre)

main()'''
    
    print("\n" + "="*50)
    print("EJEMPLO - CÓDIGO PYTHON:")
    print("="*50)
    print(example_code)
    
    try:
        js_code = compiler.compile(example_code)
        print("\n" + "="*50)
        print("CÓDIGO JAVASCRIPT GENERADO:")
        print("="*50)
        print(js_code)
        print("="*50)
        
    except CompilerError as e:
        print(f"✗ Error en el ejemplo: {e}")

def print_help():
    """Imprime ayuda del modo interactivo"""
    help_text = """
Comandos disponibles:
  help          - Muestra esta ayuda
  clear         - Limpia la pantalla
  file <nombre> - Compila un archivo Python
  example       - Muestra un ejemplo de compilación
  exit/quit     - Sale del programa
  
Para compilar código directamente:
  1. Escriba el código Python
  2. Termine con una línea vacía
  3. El código se compilará automáticamente
"""
    print(help_text)

def compile_file_cmd(input_file, output_file=None):
    """Compila un archivo desde línea de comandos"""
    compiler = PythonToJSCompiler()
    
    if output_file is None:
        output_file = input_file.replace('.py', '.js')
    
    try:
        compiler.compile_file(input_file, output_file)
        print(f"✓ Compilación exitosa: {input_file} → {output_file}")
        
    except CompilerError as e:
        print(f"✗ Error de compilación: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Traductor Python a JavaScript ES6",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py                    # Interfaz gráfica
  python main.py -i                 # Modo interactivo
  python main.py -c archivo.py      # Compilar archivo
  python main.py -c input.py -o output.js  # Especificar salida
        """
    )
    
    parser.add_argument('-c', '--compile', metavar='FILE',
                       help='Compilar archivo Python')
    parser.add_argument('-o', '--output', metavar='FILE',
                       help='Archivo de salida JavaScript')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Modo interactivo')
    
    args = parser.parse_args()
    
    if args.compile:
        compile_file_cmd(args.compile, args.output)
    elif args.interactive:
        interactive_mode()
    else:
        # Interfaz gráfica por defecto
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError as e:
            print("Error: No se pudo cargar la interfaz gráfica.")
            print("Asegúrese de tener tkinter instalado.")
            print("Usando modo interactivo...")
            interactive_mode()

if __name__ == "__main__":
    main()
