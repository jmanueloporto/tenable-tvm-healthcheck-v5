import json
import os
import subprocess
from flask import Flask, render_template, jsonify

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if "web" in BASE_DIR:
    BASE_DIR = os.path.dirname(BASE_DIR)

def load_data_safe():
    default_data = {
        "assets": {"total": 0},
        "vulnerabilities": {"total": 0},
        "sensors": {"summary": {"total": 0}, "stats_by_type": {}},
        "findings": []
    }
    json_path = os.path.join(BASE_DIR, 'reports/latest_results.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                for key in default_data:
                    if key in raw_data:
                        default_data[key] = raw_data[key]
        except Exception:
            pass
    return default_data

@app.route('/')
def index():
    return render_template('index.html', data=load_data_safe())

@app.route('/api/run-audit', methods=['POST'])
def run_audit():
    try:
        main_py = os.path.join(BASE_DIR, 'main.py')
        venv_python = os.path.join(BASE_DIR, '.venv/bin/python')
        subprocess.run([venv_python, main_py], cwd=BASE_DIR, check=True)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
