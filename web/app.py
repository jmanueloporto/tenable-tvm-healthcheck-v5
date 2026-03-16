# VERSION: 5.1.1-FINAL
from flask import Flask, render_template, jsonify
import json
import os
import subprocess

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    json_path = os.path.join(BASE_DIR, '../reports/latest_results.json')
    data = {}
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"error": "No hay datos. Lance una auditoria."}
    return render_template('index.html', data=data)

@app.route('/api/run-audit', methods=['POST'])
def run_audit():
    try:
        python_exe = '/home/adminu/mpiv/tenable-tvm-healthcheck-v5/.venv/bin/python'
        result = subprocess.run([python_exe, '../main.py'], cwd='../', capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"status": "success"})
        return jsonify({"status": "error", "message": result.stderr}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
