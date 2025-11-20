from lexer import Lexer
from parser import Parser, ParseError
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator

class CompilerError(Exception):
    pass

class PythonToJSCompiler:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.semantic_analyzer = SemanticAnalyzer()
        self.code_generator = CodeGenerator()
    
    def compile(self, python_code: str) -> str:
        """
        Compila código Python a JavaScript ES6
        """
        try:
            # Fase 1: Análisis Léxico
            print("Fase 1: Análisis Léxico...")
            self.lexer = Lexer(python_code)
            tokens = self.lexer.tokenize()
            print(f"Tokens generados: {len(tokens)}")
            
            # Fase 2: Análisis Sintáctico
            print("Fase 2: Análisis Sintáctico...")
            self.parser = Parser(tokens)
            ast = self.parser.parse()
            print("AST construido exitosamente")
            
            # Fase 3: Análisis Semántico
            print("Fase 3: Análisis Semántico...")
            errors = self.semantic_analyzer.analyze(ast)
            if errors:
                error_msg = "Errores semánticos encontrados:\n" + "\n".join(errors)
                raise CompilerError(error_msg)
            print("Análisis semántico completado")
            
            # Fase 4: Generación de Código
            print("Fase 4: Generación de Código...")
            javascript_code = self.code_generator.generate(ast)
            print("Código JavaScript generado exitosamente")
            
            return javascript_code
            
        except ParseError as e:
            raise CompilerError(f"Error de sintaxis: {e}")
        except Exception as e:
            raise CompilerError(f"Error de compilación: {e}")
    
    def compile_file(self, input_file: str, output_file: str):
        """
        Compila un archivo Python a JavaScript
        """
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                python_code = f.read()
            
            javascript_code = self.compile(python_code)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(javascript_code)
            
            print(f"Compilación exitosa: {input_file} -> {output_file}")
            
        except FileNotFoundError:
            raise CompilerError(f"Archivo no encontrado: {input_file}")
        except Exception as e:
            raise CompilerError(f"Error al procesar archivo: {e}")

def main():
    """
    Función principal para pruebas
    """
    compiler = PythonToJSCompiler()
    
    # Código Python de ejemplo más simple
    python_code = """def saludar(nombre):
    return "Hola, " + nombre

resultado = saludar("Mundo")
print(resultado)
"""
    
    try:
        js_code = compiler.compile(python_code)
        print("\n" + "="*50)
        print("CÓDIGO JAVASCRIPT GENERADO:")
        print("="*50)
        print(js_code)
    except CompilerError as e:
        print(f"Error de compilación: {e}")

if __name__ == "__main__":
    main()
