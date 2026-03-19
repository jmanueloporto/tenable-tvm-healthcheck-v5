""" VERSION: 5.4.0 | STATUS: Stable """
import json
import os
import time

class TenableDataCollector:
    def __init__(self, connection):
        self.connection = connection
        self.results = {}

    def collect_all(self):
        start_time = time.time()
        print("[*] Starting Phase 1 Silent Collection (v5.3.6-PURE_API)...")
        
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

        self.save_results()
        duration = round(time.time() - start_time, 2)
        print("-" * 60)
        print(f"[SUCCESS] Data Captured | Time: {duration}s")
        print("-" * 60)
        return self.results

    def fetch_scanners(self):
        data = self.connection.get("/scanners")
        scanners = data.get('scanners', []) if isinstance(data, dict) else []
        
        stats = {
            "Nessus Scanners": {"qty": 0, "active": 0, "inactive": 0},
            "Nessus Agents": {"qty": 0, "active": 0, "inactive": 0},
            "Nessus Network Monitors": {"qty": 0, "active": 0, "inactive": 0},
            "OT Connectors": {"qty": 0, "active": 0, "inactive": 0},
            "Web Application Scanners": {"qty": 0, "active": 0, "inactive": 0}
        }
        
        full_inventory = []
        for s in scanners:
            rtype = s.get('type', '').lower()
            name = s.get('name', 'N/A')
            status = s.get('status', 'off')
            is_on = status in ['on', 'online']
            
            # Clasificación limpia para Scanners y NNM
            if rtype in ['local', 'managed']: 
                label = "Nessus Scanners"
            elif rtype in ['pool', 'active_directory', 'agent']:
                continue # Los grupos los ignora la GUI, y los agentes se buscan en su endpoint
            elif 'pvs' in rtype or 'managed_pvs' in rtype: 
                label = "Nessus Network Monitors"
            elif 'webapp' in rtype or 'managed_webapp' in rtype: 
                label = "Web Application Scanners"
            else: 
                label = "OT Connectors"

            stats[label]["qty"] += 1
            if is_on: stats[label]["active"] += 1
            else: stats[label]["inactive"] += 1
            
            full_inventory.append({
                "name": name, 
                "label": label, 
                "raw_type": rtype, 
                "status": status
            })

        # FETCH REAL DE AGENTES
        try:
            agents_data = self.connection.get("/scanners/1/agents")
            agents = agents_data.get('agents', []) if isinstance(agents_data, dict) else []
            for a in agents:
                name = a.get('name', 'N/A')
                status = a.get('status', 'off')
                is_on = status in ['on', 'online']
                
                stats["Nessus Agents"]["qty"] += 1
                if is_on: stats["Nessus Agents"]["active"] += 1
                else: stats["Nessus Agents"]["inactive"] += 1
                
                full_inventory.append({
                    "name": name, 
                    "label": "Nessus Agents", 
                    "raw_type": "agent", 
                    "status": status
                })
        except Exception:
            pass

        # CONSULTA NATIVA DEL OT CONNECTOR (La clave del misterio)
        try:
            ot_data = self.connection.get("/sensors/ot")
            ot_connectors = ot_data if isinstance(ot_data, list) else ot_data.get('sensors', []) if isinstance(ot_data, dict) else []
            
            for ot in ot_connectors:
                name = ot.get('name', 'N/A')
                status = ot.get('status', 'off')
                is_on = status in ['on', 'online', 'connected']
                
                stats["OT Connectors"]["qty"] += 1
                if is_on: stats["OT Connectors"]["active"] += 1
                else: stats["OT Connectors"]["inactive"] += 1
                
                full_inventory.append({
                    "name": name, 
                    "label": "OT Connectors", 
                    "raw_type": "ot_connector", 
                    "status": status
                })
        except Exception as e:
            print(f"\n[WARNING] Could not fetch OT Connectors natively: {e}")

        # NINGÚN HARDCODEO AQUÍ. LO QUE DA LA API, SE MUESTRA.
        self.results['sensors'] = {
            'summary': {'total': sum(d["qty"] for d in stats.values())},
            'stats_by_type': stats,
            'inventory': full_inventory
        }

    def fetch_audit_logs(self):
        try:
            self.connection.get("/audit-log/events?limit=1")
            self.results['audit_logs'] = {"total": 1, "status": "Success"}
        except:
            self.results['audit_logs'] = {"total": 0, "status": "Forbidden"}

    def fetch_assets(self):
        try:
            data = self.connection.get("/assets")
            self.results['assets'] = {"total": data.get('total', 0) if isinstance(data, dict) else 0}
        except:
            self.results['assets'] = {"total": 0}

    def fetch_vulnerabilities(self):
        try:
            data = self.connection.get("/workbenches/vulnerabilities")
            self.results['vulnerabilities'] = {"total": len(data.get('vulnerabilities', [])) if isinstance(data, dict) else 0}
        except:
            self.results['vulnerabilities'] = {"total": 0}

    def fetch_endpoint(self, endpoint, key):
        data = self.connection.get(endpoint)
        self.results[key] = {"total": len(data.get(key, [])) if isinstance(data, dict) else 0}

    def save_results(self):
        path = "reports/latest_results.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f: json.dump(self.results, f, indent=4)
