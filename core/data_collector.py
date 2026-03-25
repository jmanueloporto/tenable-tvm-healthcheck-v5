""" VERSION: 5.5.0-STABLE | STATUS: DOMAIN 1 READY """
import json, os, time

class TenableDataCollector:
    def __init__(self, connection):
        self.connection = connection
        self.results = {}

    def collect_all(self):
        start_time = time.time()
        print("[*] Starting Data Collection (v5.5.0-DEV)...")
        
        steps = [
            ("Hybrid Sensors", self.fetch_scanners),
            ("Assets", self.fetch_assets),
            ("Scans", lambda: self.fetch_endpoint("/scans", "scans")),
            ("Policies", lambda: self.fetch_endpoint("/policies", "policies")),
            ("Vulnerabilities", self.fetch_vulnerabilities),
            ("Users", lambda: self.fetch_endpoint("/users", "users")),
            ("Audit Logs", self.fetch_audit_logs)
        ]

        for i, (name, func) in enumerate(steps, 1):
            print(f" [Step {i}/7] Fetching {name}...")
            func()

        self.results['findings'] = [] # Placeholder para dominios
        self.save_results()
        
        print("-" * 60)
        print(f"[SUCCESS] Data Captured | Time: {round(time.time() - start_time, 2)}s")
        print("-" * 60)
        return self.results

    def fetch_scanners(self):
        data = self.connection.get("/scanners")
        scanners = data.get('scanners', []) if isinstance(data, dict) else []
        stats = {k: {"qty": 0, "active": 0, "inactive": 0} for k in ["Nessus Scanners", "Nessus Agents", "Nessus Network Monitors", "OT Connectors", "Web Application Scanners"]}
        inventory = []
        for s in scanners:
            rtype = s.get('type', '').lower()
            if rtype in ['pool', 'active_directory', 'agent']: continue
            label = "Nessus Scanners"
            if 'pvs' in rtype: label = "Nessus Network Monitors"
            elif 'webapp' in rtype: label = "Web Application Scanners"
            is_on = s.get('status') == 'on'
            stats[label]["qty"] += 1
            if is_on: stats[label]["active"] += 1
            else: stats[label]["inactive"] += 1
            inventory.append({"name": s.get('name'), "label": label, "status": s.get('status')})
        
        try:
            a_data = self.connection.get("/scanners/1/agents")
            for a in a_data.get('agents', []):
                stats["Nessus Agents"]["qty"] += 1
                if a.get('status') == 'on': stats["Nessus Agents"]["active"] += 1
                else: stats["Nessus Agents"]["inactive"] += 1
                inventory.append({"name": a.get('name'), "label": "Nessus Agents", "status": a.get('status')})
        except: pass

        self.results['sensors'] = {'summary': {'total': len(inventory)}, 'stats_by_type': stats, 'inventory': inventory}

    def fetch_assets(self):
        try:
            data = self.connection.get("/assets")
            # Guardamos el total y una lista vacía para futura expansión de detalles
            self.results['assets'] = {"total": data.get('total', 0), "list": []}
        except: self.results['assets'] = {"total": 0, "list": []}

    def fetch_vulnerabilities(self):
        try:
            data = self.connection.get("/workbenches/vulnerabilities")
            self.results['vulnerabilities'] = {"total": len(data.get('vulnerabilities', []))}
        except: self.results['vulnerabilities'] = {"total": 0}

    def fetch_audit_logs(self): self.results['audit_logs'] = {"total": 0}
    
    def fetch_endpoint(self, endpoint, key):
        try:
            data = self.connection.get(endpoint)
            self.results[key] = {"total": len(data.get(key, []))}
        except: self.results[key] = {"total": 0}

    def save_results(self):
        path = "reports/latest_results.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f: json.dump(self.results, f, indent=4)
