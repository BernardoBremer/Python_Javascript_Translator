from flask import Flask, render_template, request, jsonify
from compiler import PythonToJSCompiler, CompilerError

app = Flask(__name__)
compiler = PythonToJSCompiler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        python_code = request.json.get('code', '')
        if not python_code.strip():
            return jsonify({'error': 'Por favor ingrese código Python'})
        
        js_code = compiler.compile(python_code)
        return jsonify({'success': True, 'javascript': js_code})
    
    except CompilerError as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
