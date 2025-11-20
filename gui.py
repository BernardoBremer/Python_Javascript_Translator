import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import os
from compiler import PythonToJSCompiler, CompilerError

class TranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traductor Python a JavaScript ES6")
        self.root.geometry("1200x800")
        
        self.compiler = PythonToJSCompiler()
        self.setup_ui()
    
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Traductor Python → JavaScript ES6", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de entrada (Python)
        input_frame = ttk.LabelFrame(main_frame, text="Código Python", padding="5")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        self.python_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, 
                                                    width=50, height=25, font=('Consolas', 10))
        self.python_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de botones
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=1, padx=10, sticky=(tk.N))
        
        # Botones
        ttk.Button(button_frame, text="Compilar →", command=self.compile_code,
                  style='Accent.TButton').grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="Limpiar", command=self.clear_all).grid(
            row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="Abrir Archivo", command=self.open_file).grid(
            row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="Guardar JS", command=self.save_js).grid(
            row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="Ejemplo", command=self.load_example).grid(
            row=4, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Frame de salida (JavaScript)
        output_frame = ttk.LabelFrame(main_frame, text="Código JavaScript ES6", padding="5")
        output_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.js_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                               width=50, height=25, font=('Consolas', 10))
        self.js_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame de estado
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, text="Listo para compilar", 
                                     foreground="green")
        self.status_label.grid(row=0, column=0, sticky=(tk.W))
        
        # Barra de progreso
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
    
    def compile_code(self):
        python_code = self.python_text.get("1.0", tk.END).strip()
        
        if not python_code:
            messagebox.showwarning("Advertencia", "Por favor ingrese código Python")
            return
        
        try:
            self.status_label.config(text="Compilando...", foreground="blue")
            self.progress.start()
            self.root.update()
            
            # Compilar código
            js_code = self.compiler.compile(python_code)
            
            # Mostrar resultado
            self.js_text.delete("1.0", tk.END)
            self.js_text.insert("1.0", js_code)
            
            self.status_label.config(text="Compilación exitosa", foreground="green")
            
        except CompilerError as e:
            self.status_label.config(text="Error de compilación", foreground="red")
            messagebox.showerror("Error de Compilación", str(e))
            
        except Exception as e:
            self.status_label.config(text="Error inesperado", foreground="red")
            messagebox.showerror("Error", f"Error inesperado: {e}")
        
        finally:
            self.progress.stop()
    
    def clear_all(self):
        self.python_text.delete("1.0", tk.END)
        self.js_text.delete("1.0", tk.END)
        self.status_label.config(text="Listo para compilar", foreground="green")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Abrir archivo Python",
            filetypes=[("Archivos Python", "*.py"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.python_text.delete("1.0", tk.END)
                self.python_text.insert("1.0", content)
                
                self.status_label.config(text=f"Archivo cargado: {os.path.basename(file_path)}", 
                                       foreground="blue")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")
    
    def save_js(self):
        js_code = self.js_text.get("1.0", tk.END).strip()
        
        if not js_code:
            messagebox.showwarning("Advertencia", "No hay código JavaScript para guardar")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Guardar código JavaScript",
            defaultextension=".js",
            filetypes=[("Archivos JavaScript", "*.js"), ("Todos los archivos", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(js_code)
                
                self.status_label.config(text=f"Archivo guardado: {os.path.basename(file_path)}", 
                                       foreground="blue")
                messagebox.showinfo("Éxito", "Archivo guardado exitosamente")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
    
    def load_example(self):
        example_code = '''def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

def main():
    print("Calculadora de Factorial y Fibonacci")
    
    for i in range(1, 6):
        fact = factorial(i)
        fib = fibonacci(i)
        print(f"factorial({i}) = {fact}")
        print(f"fibonacci({i}) = {fib}")

main()'''
        
        self.python_text.delete("1.0", tk.END)
        self.python_text.insert("1.0", example_code)
        self.status_label.config(text="Ejemplo cargado", foreground="blue")

def main():
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
