""" VERSION: 5.5.0-STABLE | STATUS: DOMAIN 1 READY """
from flask import Flask, render_template, jsonify
import json, os, subprocess

app = Flask(__name__)
BASE_DIR = "/home/adminu/mpiv/tenable-tvm-healthcheck-v5"

def get_safe_data():
    """Garantiza que el Dashboard siempre tenga variables validas"""
    default = {
        "assets": {"total": 0},
        "vulnerabilities": {"total": 0},
        "sensors": {"summary": {"total": 0}, "stats_by_type": {}},
        "findings": []
    }
    json_path = os.path.join(BASE_DIR, 'reports/latest_results.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                # Fusionar con el default para asegurar llaves faltantes
                for key in default:
                    if key in raw: default[key] = raw[key]
        except: pass
    return default

@app.route('/')
def index():
    return render_template('index.html', data=get_safe_data())

@app.route('/api/run-audit', methods=['POST'])
def run_audit():
    try:
        main_py = os.path.join(BASE_DIR, 'main.py')
        venv_python = os.path.join(BASE_DIR, '.venv/bin/python')
        # Ejecución atómica
        subprocess.run([venv_python, main_py], cwd=BASE_DIR, check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
