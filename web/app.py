""" VERSION: 5.4.2 | STATUS: STABLE - PURE API ARCHITECTURE & MTTR ENGINE """
from flask import Flask, render_template, jsonify
import json, os, subprocess

app = Flask(__name__)
# Definimos la ruta raiz de tu proyecto de forma absoluta
BASE_DIR = "/home/adminu/mpiv/tenable-tvm-healthcheck-v5"

@app.route('/')
def index():
    json_path = os.path.join(BASE_DIR, 'reports/latest_results.json')
    
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"error": "JSON file missing. Please run main.py first."}
    
    return render_template('index.html', data=data)

@app.route('/api/run-audit', methods=['POST'])
def run_audit():
    try:
        main_py = os.path.join(BASE_DIR, 'main.py')
        venv_python = os.path.join(BASE_DIR, '.venv/bin/python')
        # Ejecuta la auditoria en segundo plano
        subprocess.run([venv_python, main_py], cwd=BASE_DIR, check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Escucha en el puerto 8080 para tu entorno Linux
    app.run(host='0.0.0.0', port=8080, debug=True)
